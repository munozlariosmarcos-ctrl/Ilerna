import logging
import requests
from django.core.cache import cache

logger = logging.getLogger(__name__)

CHEAPSHARK_URL = "https://www.cheapshark.com/api/1.0/games"
CACHE_TTL = 60 * 10  # 10 minutos


class CatalogServiceError(Exception):
    def __init__(self, error, status):
        self.error = error
        self.status = status
        super().__init__(error)


def _fetch_search(q):
    """Llama a CheapShark para buscar juegos por título."""
    logger.info("Consultando proveedor externo | action=search q=%s", q)
    try:
        response = requests.get(
            CHEAPSHARK_URL,
            params={"title": q, "limit": 20},
            timeout=5,
        )
    except requests.Timeout:
        logger.error("Timeout al consultar proveedor | action=search q=%s", q)
        raise CatalogServiceError("external_service_unavailable", 503)
    except requests.ConnectionError:
        logger.error("Error de red al consultar proveedor | action=search q=%s", q)
        raise CatalogServiceError("external_service_unavailable", 503)

    if not response.ok:
        logger.error(
            "Proveedor respondió con error | action=search q=%s status_code=%s",
            q, response.status_code,
        )
        raise CatalogServiceError("external_service_error", 502)

    try:
        games = response.json()
        if not isinstance(games, list):
            raise ValueError("Respuesta inválida")
    except Exception:
        logger.error("Respuesta inválida del proveedor | action=search q=%s", q)
        raise CatalogServiceError("external_service_error", 502)

    logger.info(
        "Proveedor respondió correctamente | action=search q=%s results=%s",
        q, len(games),
    )

    return [
        {
            "external_game_id": str(game["gameID"]),
            "title": game["external"],
            "thumb": game["thumb"],
        }
        for game in games
    ]


def search_games(q):
    cache_key = f"catalog:search:{q.lower().strip()}"

    # Consulta Redis
    cached = cache.get(cache_key)
    if cached is not None:
        logger.info(
            "Datos obtenidos desde Redis | action=search q=%s origen=cache resultado=ok",
            q,
        )
        return cached

    logger.info(
        "No hay datos en Redis, consultando proveedor | action=search q=%s origen=proveedor",
        q,
    )

    # Llamar a CheapShark
    try:
        results = _fetch_search(q)
        cache.set(cache_key, results, timeout=CACHE_TTL)
        logger.info(
            "Datos guardados en Redis | action=search q=%s ttl=%ss",
            q, CACHE_TTL,
        )
        return results
    except CatalogServiceError as e:
        # Si falla CheapShark, intentar usar datos stale de Redis
        stale = cache.get(cache_key)
        if stale is not None:
            logger.warning(
                "Proveedor falló, usando datos cacheados | action=search q=%s origen=cache_fallback error=%s resultado=ok",
                q, e.error,
            )
            return stale
        logger.error(
            "Proveedor falló y no hay datos en Redis | action=search q=%s error=%s resultado=error",
            q, e.error,
        )
        raise


def resolve_games(ids):
    results = []
    for game_id in ids:
        logger.info("Consultando proveedor externo | action=resolve game_id=%s", game_id)
        try:
            response = requests.get(
                CHEAPSHARK_URL,
                params={"id": game_id},
                timeout=5,
            )
        except requests.Timeout:
            logger.error("Timeout al consultar proveedor | action=resolve game_id=%s", game_id)
            raise CatalogServiceError("external_service_unavailable", 503)
        except requests.ConnectionError:
            logger.error("Error de red al consultar proveedor | action=resolve game_id=%s", game_id)
            raise CatalogServiceError("external_service_unavailable", 503)

        if not response.ok:
            logger.error(
                "Proveedor respondió con error | action=resolve game_id=%s status_code=%s",
                game_id, response.status_code,
            )
            raise CatalogServiceError("external_service_error", 502)

        try:
            game = response.json()
            if game and "info" in game:
                results.append({
                    "external_game_id": game_id,
                    "title": game["info"]["title"],
                    "thumb": game["info"]["thumb"],
                })
                logger.info(
                    "Juego resuelto correctamente | action=resolve game_id=%s resultado=ok",
                    game_id,
                )
        except Exception:
            logger.error("Respuesta inválida del proveedor | action=resolve game_id=%s", game_id)
            raise CatalogServiceError("external_service_error", 502)

    return results


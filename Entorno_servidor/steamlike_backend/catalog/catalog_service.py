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
    try:
        response = requests.get(
            CHEAPSHARK_URL,
            params={"title": q, "limit": 20},
            timeout=5,
        )
    except requests.Timeout:
        raise CatalogServiceError("external_service_unavailable", 503)
    except requests.ConnectionError:
        raise CatalogServiceError("external_service_unavailable", 503)

    if not response.ok:
        raise CatalogServiceError("external_service_error", 502)

    try:
        games = response.json()
        if not isinstance(games, list):
            raise ValueError("Respuesta inválida")
    except Exception:
        raise CatalogServiceError("external_service_error", 502)

    return [
        {
            "external_game_id": str(game["gameID"]),
            "title": game["external"],
            "thumb": game["thumb"],
        }
        for game in games
    ]


def search_games(q):
    """
    Busca juegos por título.
    1. Consulta Redis — si hay datos los devuelve directamente.
    2. Si no hay datos en Redis — llama a CheapShark.
    3. Si CheapShark falla pero hay datos stale en Redis — los usa.
    4. Si CheapShark falla y no hay datos — propaga el error.
    """
    cache_key = f"catalog:search:{q.lower().strip()}"

    # Comprobar Redis
    cached = cache.get(cache_key)
    if cached is not None:
        logger.info("Cache HIT para búsqueda | q=%s", q)
        return cached

    logger.info("Cache MISS para búsqueda | q=%s", q)

    # Llamar a CheapShark
    try:
        results = _fetch_search(q)
        cache.set(cache_key, results, timeout=CACHE_TTL)
        return results
    except CatalogServiceError as e:
        # Si falla CheapShark, intentar usar datos stale de Redis
        stale = cache.get(cache_key)
        if stale is not None:
            logger.warning(
                "CheapShark falló pero se usan datos cacheados | q=%s error=%s",
                q, e.error,
            )
            return stale
        logger.error("CheapShark falló y no hay datos en caché | q=%s error=%s", q, e.error)
        raise


def resolve_games(ids):
    """
    Resuelve una lista de IDs externos consultando CheapShark.
    Devuelve lista de dicts con external_game_id, title, thumb.
    """
    results = []
    for game_id in ids:
        try:
            response = requests.get(
                CHEAPSHARK_URL,
                params={"id": game_id},
                timeout=5,
            )
        except requests.Timeout:
            raise CatalogServiceError("external_service_unavailable", 503)
        except requests.ConnectionError:
            raise CatalogServiceError("external_service_unavailable", 503)

        if not response.ok:
            raise CatalogServiceError("external_service_error", 502)

        try:
            game = response.json()
            if game and "info" in game:
                results.append({
                    "external_game_id": game_id,
                    "title": game["info"]["title"],
                    "thumb": game["info"]["thumb"],
                })
        except Exception:
            raise CatalogServiceError("external_service_error", 502)

    return results
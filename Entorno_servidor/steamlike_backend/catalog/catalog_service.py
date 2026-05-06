import requests
from django.core.cache import cache

CHEAPSHARK_URL = "https://www.cheapshark.com/api/1.0/games"
CACHE_TTL = 60 * 10  # 10 minutos


class CatalogServiceError(Exception):
    def __init__(self, error, status):
        self.error = error
        self.status = status
        super().__init__(error)


def search_games(q):
    """
    Busca juegos por título.
    Primero consulta Redis, si no está llama a CheapShark.
    Devuelve lista de dicts con external_game_id, title, thumb.
    """
    cache_key = f"catalog:search:{q.lower().strip()}"

    cached = cache.get(cache_key)
    if cached is not None:
        return cached

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

    results = [
        {
            "external_game_id": str(game["gameID"]),
            "title": game["external"],
            "thumb": game["thumb"],
        }
        for game in games
    ]

    cache.set(cache_key, results, timeout=CACHE_TTL)
    return results


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
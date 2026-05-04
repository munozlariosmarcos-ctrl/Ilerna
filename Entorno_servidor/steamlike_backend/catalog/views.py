import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from steamlike_backend.utils import error_400, error_502, error_503

CHEAPSHARK_SEARCH_URL = "https://www.cheapshark.com/api/1.0/games"


@require_GET
def search(request):
    q = request.GET.get("q", None)

    if q is None:
        return error_400([{"field": "q", "message": "El parámetro 'q' es obligatorio."}])
    if not q.strip():
        return error_400([{"field": "q", "message": "El parámetro 'q' no puede estar vacío."}])

    # Caso A — timeout o error de red
    try:
        response = requests.get(
            CHEAPSHARK_SEARCH_URL,
            params={"title": q, "limit": 20},
            timeout=5,
        )
    except requests.Timeout:
        return error_503()
    except requests.ConnectionError:
        return error_503()

    # Caso B — respuesta con error o datos no válidos
    if not response.ok:
        return error_502()

    try:
        games = response.json()
        if not isinstance(games, list):
            return error_502()
    except Exception:
        return error_502()

    results = [
        {
            "external_game_id": str(game["gameID"]),
            "title": game["external"],
            "thumb": game["thumb"],
        }
        for game in games
    ]

    return JsonResponse(results, safe=False, status=200)


@csrf_exempt
@require_http_methods(["POST"])
def resolve(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return error_400([{"field": "body", "message": "El body debe ser un JSON válido."}])

    if not data:
        return error_400([{"field": "external_game_ids", "message": "El campo 'external_game_ids' es obligatorio."}])

    if "external_game_ids" not in data:
        return error_400([{"field": "external_game_ids", "message": "El campo 'external_game_ids' es obligatorio."}])

    ids = data["external_game_ids"]

    if not isinstance(ids, list):
        return error_400([{"field": "external_game_ids", "message": "'external_game_ids' debe ser una lista."}])

    if len(ids) == 0:
        return error_400([{"field": "external_game_ids", "message": "'external_game_ids' no puede estar vacía."}])

    if not all(isinstance(i, str) for i in ids):
        return error_400([{"field": "external_game_ids", "message": "Todos los elementos deben ser strings."}])

    results = []
    for game_id in ids:
        # Caso A — timeout o error de red
        try:
            response = requests.get(
                CHEAPSHARK_SEARCH_URL,
                params={"id": game_id},
                timeout=5,
            )
        except requests.Timeout:
            return error_503()
        except requests.ConnectionError:
            return error_503()

        # Caso B — respuesta con error o datos no válidos
        if not response.ok:
            return error_502()

        try:
            game = response.json()
            if game and "info" in game:
                results.append({
                    "external_game_id": game_id,
                    "title": game["info"]["title"],
                    "thumb": game["info"]["thumb"],
                })
        except Exception:
            return error_502()

    return JsonResponse(results, safe=False, status=200)
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from steamlike_backend.utils import error_400

CHEAPSHARK_SEARCH_URL = "https://www.cheapshark.com/api/1.0/games"


@require_GET
def search(request):
    q = request.GET.get("q", None)

    # Validar q
    if q is None:
        return error_400([{"field": "q", "message": "El parámetro 'q' es obligatorio."}])
    if not q.strip():
        return error_400([{"field": "q", "message": "El parámetro 'q' no puede estar vacío."}])

    # Llamar a CheapShark
    try:
        response = requests.get(
            CHEAPSHARK_SEARCH_URL,
            params={"title": q, "limit": 20},
            timeout=5,
        )
        response.raise_for_status()
        games = response.json()
    except Exception:
        return JsonResponse([], safe=False, status=200)

    # Formatear respuesta
    results = [
        {
            "external_game_id": str(game["gameID"]),
            "title": game["external"],
            "thumb": game["thumb"],
        }
        for game in games
    ]

    return JsonResponse(results, safe=False, status=200)
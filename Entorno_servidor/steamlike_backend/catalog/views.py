import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from steamlike_backend.utils import error_400
from .catalog_service import search_games, resolve_games, CatalogServiceError

ERRORS = {
    503: lambda: JsonResponse(
        {"error": "external_service_unavailable", "message": "El catálogo externo no está disponible. Inténtalo más tarde."},
        status=503,
    ),
    502: lambda: JsonResponse(
        {"error": "external_service_error", "message": "Error al consultar el catálogo externo."},
        status=502,
    ),
}


@require_GET
def search(request):
    q = request.GET.get("q", None)

    if q is None:
        return error_400([{"field": "q", "message": "El parámetro 'q' es obligatorio."}])
    if not q.strip():
        return error_400([{"field": "q", "message": "El parámetro 'q' no puede estar vacío."}])

    try:
        results = search_games(q)
    except CatalogServiceError as e:
        return ERRORS[e.status]()

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

    try:
        results = resolve_games(ids)
    except CatalogServiceError as e:
        return ERRORS[e.status]()

    return JsonResponse(results, safe=False, status=200)
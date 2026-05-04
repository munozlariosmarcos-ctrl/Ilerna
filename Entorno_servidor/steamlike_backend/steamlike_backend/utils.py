from django.http import JsonResponse


def error_400(errors):
    details = {e["field"]: e["message"] for e in errors}
    return JsonResponse(
        {
            "error": "validation_error",
            "message": "Datos de entrada inválidos",
            "details": details,
        },
        status=400,
    )


def error_401(message="No autenticado"):
    return JsonResponse(
        {
            "error": "unauthorized",
            "message": message,
        },
        status=401,
    )


def error_404(message="La entrada solicitada no existe"):
    return JsonResponse(
        {
            "error": "not_found",
            "message": message,
        },
        status=404,
    )


def error_502():
    return JsonResponse(
        {
            "error": "external_service_error",
            "message": "Error al consultar el catálogo externo.",
        },
        status=502,
    )


def error_503():
    return JsonResponse(
        {
            "error": "external_service_unavailable",
            "message": "El catálogo externo no está disponible. Inténtalo más tarde.",
        },
        status=503,
    )


def error_invalid_external_game_id():
    return JsonResponse(
        {
            "error": "invalid_external_game_id",
            "message": "El juego indicado no existe en el catálogo externo.",
            "details": {"external_game_id": "not_found"},
        },
        status=400,
    )
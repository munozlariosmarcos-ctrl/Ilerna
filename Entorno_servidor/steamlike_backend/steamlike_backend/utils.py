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
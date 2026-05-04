from django.shortcuts import render

# Create your views here.
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from steamlike_backend.email_service import send_email, EmailServiceError
from steamlike_backend.utils import error_400


def _error_503():
    return JsonResponse(
        {
            "error": "external_service_unavailable",
            "message": "El servicio de email no está disponible. Inténtalo más tarde.",
        },
        status=503,
    )


def _error_502():
    return JsonResponse(
        {
            "error": "external_service_error",
            "message": "Error al enviar el email.",
        },
        status=502,
    )


@csrf_exempt
@require_http_methods(["POST"])
def test_email(request):
    # Solo disponible en DEBUG — si no, 404
    if not settings.DEBUG:
        from django.http import Http404
        raise Http404

    # Parsear JSON
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return error_400([{"field": "body", "message": "El body debe ser un JSON válido."}])

    if not data:
        return error_400([{"field": "body", "message": "El body no puede estar vacío. Se requieren: to, subject, text."}])

    # Validar campos
    errors = []

    if "to" not in data:
        errors.append({"field": "to", "message": "El campo 'to' es obligatorio."})
    elif not isinstance(data["to"], str) or not data["to"].strip():
        errors.append({"field": "to", "message": "'to' debe ser un string no vacío."})

    if "subject" not in data:
        errors.append({"field": "subject", "message": "El campo 'subject' es obligatorio."})
    elif not isinstance(data["subject"], str) or not data["subject"].strip():
        errors.append({"field": "subject", "message": "'subject' debe ser un string no vacío."})

    if "text" not in data:
        errors.append({"field": "text", "message": "El campo 'text' es obligatorio."})
    elif not isinstance(data["text"], str) or not data["text"].strip():
        errors.append({"field": "text", "message": "'text' debe ser un string no vacío."})

    if errors:
        return error_400(errors)

    # Enviar email
    try:
        send_email(
            to=data["to"],
            subject=data["subject"],
            text=data["text"],
        )
    except EmailServiceError as e:
        if e.status == 503:
            return _error_503()
        return _error_502()

    return JsonResponse({"ok": True}, status=200)
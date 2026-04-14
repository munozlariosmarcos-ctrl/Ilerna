import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

User = get_user_model()


# ── helpers ──────────────────────────────────────────────────────────────────

def _error_400(errors):
    details = {e["field"]: e["message"] for e in errors}
    return JsonResponse(
        {
            "error": "validation_error",
            "message": "Datos de entrada inválidos",
            "details": details,
        },
        status=400,
    )


def _validate_register(data):
    errors = []

    # username
    if "username" not in data:
        errors.append({"field": "username", "message": "El campo 'username' es obligatorio."})
    elif not isinstance(data["username"], str) or not data["username"].strip():
        errors.append({"field": "username", "message": "'username' debe ser un string no vacío."})

    # password
    if "password" not in data:
        errors.append({"field": "password", "message": "El campo 'password' es obligatorio."})
    elif not isinstance(data["password"], str):
        errors.append({"field": "password", "message": "'password' debe ser un string."})
    elif len(data["password"]) < 8:
        errors.append({"field": "password", "message": "'password' debe tener al menos 8 caracteres."})

    return errors


# ── POST /api/auth/register/ ──────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    # Parsear JSON
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return _error_400([{"field": "body", "message": "El body debe ser un JSON válido."}])

    # Body vacío
    if not data:
        return _error_400([{"field": "body", "message": "El body no puede estar vacío. Se requieren: username, password."}])

    # Validaciones de campos
    errors = _validate_register(data)
    if errors:
        return _error_400(errors)

    # Username duplicado
    if User.objects.filter(username=data["username"]).exists():
        return _error_400([{"field": "username", "message": "El username ya está en uso."}])

    # Crear usuario (create_user hashea la password automáticamente)
    user = User.objects.create_user(
        username=data["username"],
        password=data["password"],
    )

    return JsonResponse(
        {
            "id": user.id,
            "username": user.username,
        },
        status=201,
    )
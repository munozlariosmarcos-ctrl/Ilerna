import json

from django.contrib.auth import authenticate, login, get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET

User = get_user_model()


# ── helpers ──────────────────────────────────────────────────────────────────

def _json_error(error, message, status, details=None):
    response = {
        "error": error,
        "message": message,
    }
    if details:
        response["details"] = details
    return JsonResponse(response, status=status)


def _parse_json(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return None, _json_error(
            "validation_error",
            "El body debe ser un JSON válido",
            400,
            {"body": "invalid_json"},
        )

    if not data:
        return None, _json_error(
            "validation_error",
            "El body no puede estar vacío",
            400,
            {"body": "empty"},
        )

    return data, None


def _serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
    }


def _require_auth(request):
    if not request.user.is_authenticated:
        return _json_error("unauthorized", "No autenticado", 401)
    return None


# ── validaciones ──────────────────────────────────────────────────────────────

def _validate_auth(data, require_password_length=False):
    errors = []

    def add(field, msg):
        errors.append({"field": field, "message": msg})

    if "username" not in data:
        add("username", "Campo obligatorio")
    elif not isinstance(data["username"], str) or not data["username"].strip():
        add("username", "Debe ser string no vacío")

    if "password" not in data:
        add("password", "Campo obligatorio")
    elif not isinstance(data["password"], str):
        add("password", "Debe ser string")
    elif require_password_length and len(data["password"]) < 8:
        add("password", "Debe tener al menos 8 caracteres")

    return errors


def _validate_password_change(data):
    errors = []

    def add(field, msg):
        errors.append({"field": field, "message": msg})

    if "current_password" not in data:
        add("current_password", "Campo obligatorio")
    elif not isinstance(data["current_password"], str):
        add("current_password", "Debe ser string")

    if "new_password" not in data:
        add("new_password", "Campo obligatorio")
    elif not isinstance(data["new_password"], str):
        add("new_password", "Debe ser string")
    elif len(data["new_password"]) < 8:
        add("new_password", "Debe tener al menos 8 caracteres")

    return errors


def _format_errors(errors):
    return {e["field"]: e["message"] for e in errors}


# ── POST /api/auth/register/ ──────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    data, error = _parse_json(request)
    if error:
        return error

    errors = _validate_auth(data, require_password_length=True)
    if errors:
        return _json_error("validation_error", "Datos inválidos", 400, _format_errors(errors))

    if User.objects.filter(username=data["username"]).exists():
        return _json_error(
            "validation_error",
            "Username en uso",
            400,
            {"username": "duplicate"},
        )

    user = User.objects.create_user(
        username=data["username"],
        password=data["password"],
    )

    return JsonResponse(_serialize_user(user), status=201)


# ── POST /api/auth/login/ ─────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    data, error = _parse_json(request)
    if error:
        return error

    errors = _validate_auth(data)
    if errors:
        return _json_error("validation_error", "Datos inválidos", 400, _format_errors(errors))

    user = authenticate(
        request,
        username=data["username"],
        password=data["password"],
    )

    if user is None:
        return _json_error("unauthorized", "Credenciales incorrectas", 401)

    login(request, user)

    return JsonResponse(_serialize_user(user), status=200)


# ── GET /api/users/me/ ────────────────────────────────────────────────────────

@require_GET
def me(request):
    auth_error = _require_auth(request)
    if auth_error:
        return auth_error

    return JsonResponse(_serialize_user(request.user), status=200)


# ── POST /api/users/me/password/ ─────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def change_password(request):
    auth_error = _require_auth(request)
    if auth_error:
        return auth_error

    data, error = _parse_json(request)
    if error:
        return error

    errors = _validate_password_change(data)
    if errors:
        return _json_error("validation_error", "Datos inválidos", 400, _format_errors(errors))

    user = authenticate(
        request,
        username=request.user.username,
        password=data["current_password"],
    )

    if user is None:
        return _json_error(
            "validation_error",
            "Contraseña incorrecta",
            400,
            {"current_password": "incorrect"},
        )

    user.set_password(data["new_password"])
    user.save()

    return JsonResponse({"ok": True}, status=200)
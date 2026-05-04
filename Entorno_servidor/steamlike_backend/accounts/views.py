import json
import logging

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET

from steamlike_backend.email_service import send_email, EmailServiceError

User = get_user_model()
logger = logging.getLogger(__name__)


# ── helpers ──────────────────────────────────────────────────────────────────
def _json_error(error, message, status, details=None):
    response = {"error": error, "message": message}
    if details:
        response["details"] = details
    return JsonResponse(response, status=status)

def _parse_json(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return None, _json_error("validation_error", "El body debe ser un JSON válido", 400, {"body": "invalid_json"})
    if not data:
        return None, _json_error("validation_error", "El body no puede estar vacío", 400, {"body": "empty"})
    return data, None

def _serialize_user(user):
    return {"id": user.id, "username": user.username, "email": user.email}

def _validate_auth(data, require_password_length=False, require_email=False):
    errors = []
    def add(field, msg): errors.append({"field": field, "message": msg})

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

    if require_email:
        if "email" not in data:
            add("email", "Campo obligatorio")
        elif not isinstance(data["email"], str) or not data["email"].strip():
            add("email", "Debe ser string no vacío")
        elif "@" not in data["email"]:
            add("email", "Debe contener una @ válida")

    return errors

def _require_auth(request):
    if not request.user.is_authenticated:
        return _json_error("unauthorized", "No autenticado", 401)
    return None


# ── POST /api/auth/register/ ──────────────────────────────────────────────────
@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    data, error = _parse_json(request)
    if error: return error

    errors = _validate_auth(data, require_password_length=True, require_email=True)
    if errors:
        return _json_error("validation_error", "Datos inválidos", 400, {e["field"]: e["message"] for e in errors})

    if User.objects.filter(username=data["username"]).exists():
        return _json_error("validation_error", "Username en uso", 400, {"username": "duplicate"})

    if User.objects.filter(email=data["email"]).exists():
        return _json_error("validation_error", "Email ya en uso", 400, {"email": "duplicate"})

    user = User.objects.create_user(
        username=data["username"],
        password=data["password"],
        email=data["email"],
    )

    # Enviar email de bienvenida — si falla, el usuario se crea igualmente
    try:
        send_email(
            to=user.email,
            subject="¡Bienvenido a GameShelf!",
            text=f"Hola {user.username}, tu cuenta ha sido creada correctamente.",
            html=f"<h1>¡Bienvenido, {user.username}!</h1><p>Tu cuenta en GameShelf ha sido creada correctamente.</p>",
            action="register_welcome",
            user=user,
        )
    except EmailServiceError as e:
        logger.error(
            "Fallo al enviar email de bienvenida | action=register_welcome user_id=%s username=%s result=error tipo=%s",
            user.id, user.username, e.error,
        )

    return JsonResponse(_serialize_user(user), status=201)


# ── POST /api/auth/login/ ─────────────────────────────────────────────────────
@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    data, error = _parse_json(request)
    if error: return error

    errors = _validate_auth(data)
    if errors:
        return _json_error("validation_error", "Datos inválidos", 400, {e["field"]: e["message"] for e in errors})

    user = authenticate(request, username=data["username"], password=data["password"])
    if user is None:
        return _json_error("unauthorized", "Credenciales incorrectas", 401)

    login(request, user)
    return JsonResponse({"id": user.id, "username": user.username}, status=200)


# ── GET /api/users/me/ ────────────────────────────────────────────────────────
@require_GET
def me(request):
    auth_error = _require_auth(request)
    if auth_error: return auth_error
    return JsonResponse(_serialize_user(request.user), status=200)


# ── POST /api/auth/logout/ ────────────────────────────────────────────────────
@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({}, status=204)


# ── POST /api/users/me/password/ ─────────────────────────────────────────────
@csrf_exempt
@require_http_methods(["POST"])
def change_password(request):
    auth_error = _require_auth(request)
    if auth_error: return auth_error

    data, error = _parse_json(request)
    if error: return error

    errors = []
    if "current_password" not in data:
        errors.append({"field": "current_password", "message": "El campo 'current_password' es obligatorio."})
    elif not isinstance(data["current_password"], str):
        errors.append({"field": "current_password", "message": "'current_password' debe ser un string."})

    if "new_password" not in data:
        errors.append({"field": "new_password", "message": "El campo 'new_password' es obligatorio."})
    elif not isinstance(data["new_password"], str):
        errors.append({"field": "new_password", "message": "'new_password' debe ser un string."})
    elif len(data["new_password"]) < 8:
        errors.append({"field": "new_password", "message": "'new_password' debe tener al menos 8 caracteres."})

    if errors:
        return _json_error("validation_error", "Datos inválidos", 400, {e["field"]: e["message"] for e in errors})

    user = authenticate(request, username=request.user.username, password=data["current_password"])
    if user is None:
        return _json_error("validation_error", "Datos inválidos", 400, {"current_password": "La contraseña actual es incorrecta."})

    user.set_password(data["new_password"])
    user.save()

    return JsonResponse({"ok": True}, status=200)
import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .models import LibraryEntry


ALLOWED_STATUSES = LibraryEntry.ALLOWED_STATUSES


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
            "El body debe ser un JSON válido.",
            400,
            {"body": "invalid_json"},
        )

    if not data:
        return None, _json_error(
            "validation_error",
            "El body no puede estar vacío.",
            400,
            {"body": "empty"},
        )

    return data, None


def _serialize_entry(entry):
    return {
        "id": entry.id,
        "external_game_id": entry.external_game_id,
        "status": entry.status,
        "hours_played": entry.hours_played,
    }


def _validate_entry(data, partial=False):
    errors = []

    def add(field, msg):
        errors.append({"field": field, "message": msg})

    # external_game_id (solo en POST)
    if not partial:
        if "external_game_id" not in data:
            add("external_game_id", "Campo obligatorio")
        elif not isinstance(data["external_game_id"], str) or not data["external_game_id"].strip():
            add("external_game_id", "Debe ser string no vacío")

    # status
    if "status" in data:
        if not isinstance(data["status"], str):
            add("status", "Debe ser string")
        elif data["status"] not in ALLOWED_STATUSES:
            add("status", f"Debe ser uno de: {', '.join(ALLOWED_STATUSES)}")

    elif not partial:
        add("status", "Campo obligatorio")

    # hours_played
    if "hours_played" in data:
        if not isinstance(data["hours_played"], int) or isinstance(data["hours_played"], bool):
            add("hours_played", "Debe ser integer")
        elif data["hours_played"] < 0:
            add("hours_played", "Debe ser >= 0")

    elif not partial:
        add("hours_played", "Campo obligatorio")

    return errors


def _require_auth(request):
    if not request.user.is_authenticated:
        return _json_error("unauthorized", "No autenticado", 401)
    return None


# ── health ───────────────────────────────────────────────────────────────────

@require_GET
def health(request):
    return JsonResponse({"status": "ok"})


# ── /api/library/entries/ ─────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["GET", "POST"])
def library_entries(request):

    auth_error = _require_auth(request)
    if auth_error:
        return auth_error

    if request.method == "GET":
        entries = LibraryEntry.objects.filter(user=request.user)
        return JsonResponse(
            [_serialize_entry(e) for e in entries],
            safe=False,
            status=200,
        )

    # POST
    data, error = _parse_json(request)
    if error:
        return error

    errors = _validate_entry(data)
    if errors:
        return _json_error(
            "validation_error",
            "Datos inválidos",
            400,
            {e["field"]: e["message"] for e in errors},
        )

    try:
        entry = LibraryEntry.objects.create(
            external_game_id=data["external_game_id"],
            status=data["status"],
            hours_played=data["hours_played"],
            user=request.user,
        )
    except IntegrityError:
        return _json_error(
            "duplicate_entry",
            "El juego ya existe en la biblioteca",
            400,
            {"external_game_id": "duplicate"},
        )

    return JsonResponse(_serialize_entry(entry), status=201)


# ── /api/library/entries/{id}/ ────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["GET", "PATCH"])
def library_entry_by_id(request, id):

    auth_error = _require_auth(request)
    if auth_error:
        return auth_error

    try:
        entry = LibraryEntry.objects.get(pk=id, user=request.user)
    except LibraryEntry.DoesNotExist:
        return _json_error("not_found", "No existe", 404)

    if request.method == "GET":
        return JsonResponse(_serialize_entry(entry), status=200)

    # PATCH
    data, error = _parse_json(request)
    if error:
        return error

    allowed_fields = {"status", "hours_played"}
    unknown = set(data.keys()) - allowed_fields
    if unknown:
        return _json_error(
            "validation_error",
            "Campos no permitidos",
            400,
            {f: "not_allowed" for f in unknown},
        )

    errors = _validate_entry(data, partial=True)
    if errors:
        return _json_error(
            "validation_error",
            "Datos inválidos",
            400,
            {e["field"]: e["message"] for e in errors},
        )

    for field in allowed_fields:
        if field in data:
            setattr(entry, field, data[field])

    entry.save()

    return JsonResponse(_serialize_entry(entry), status=200)
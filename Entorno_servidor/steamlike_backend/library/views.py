import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

import requests
from steamlike_backend.utils import error_400, error_401, error_404, error_502, error_503, error_invalid_external_game_id



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

def _check_external_game_exists(external_game_id):
    try:
        response = requests.get(
            "https://www.cheapshark.com/api/1.0/games",
            params={"id": external_game_id},
            timeout=5,
        )
    except requests.Timeout:
        return error_503()
    except requests.ConnectionError:
        return error_503()

    # Si CheapShark devuelve 404 o similar → juego no existe
    if response.status_code == 404:
        return error_invalid_external_game_id()

    # Cualquier otro error del servidor
    if not response.ok:
        return error_502()

    try:
        game = response.json()
        if not game or "info" not in game:
            return error_invalid_external_game_id()
    except Exception:
        return error_502()

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

    # Validar que el juego existe en CheapShark ← añadir esto
    external_error = _check_external_game_exists(data["external_game_id"])
    if external_error:
        return external_error

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
@require_http_methods(["GET", "PATCH", "PUT"])  # ← añadir "PUT"
def library_entry_by_id(request, id):

    if not request.user.is_authenticated:
        return error_401()

    try:
        entry = LibraryEntry.objects.get(pk=id, user=request.user)
    except LibraryEntry.DoesNotExist:
        return error_404()

    if request.method == "GET":
        return JsonResponse(
            {
                "id": entry.id,
                "external_game_id": entry.external_game_id,
                "status": entry.status,
                "hours_played": entry.hours_played,
            },
            status=200,
        )

    # PUT — sustituir todos los campos
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return error_400([{"field": "body", "message": "El body debe ser un JSON válido."}])

        if not data:
            return error_400([{"field": "body", "message": "El body no puede estar vacío. Se requieren: external_game_id, status, hours_played."}])

        errors = _validate_entry(data)
        if errors:
            return error_400(errors)

        entry.external_game_id = data["external_game_id"]
        entry.status = data["status"]
        entry.hours_played = data["hours_played"]
        entry.save()

        return JsonResponse(
            {
                "id": entry.id,
                "external_game_id": entry.external_game_id,
                "status": entry.status,
                "hours_played": entry.hours_played,
            },
            status=200,
        )

    # PATCH — actualizar solo los campos enviados
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return error_400([{"field": "body", "message": "El body debe ser un JSON válido."}])

    if not data:
        return error_400([{"field": "body", "message": "El body no puede estar vacío. Se requieren: status y/o hours_played."}])

    unknown = set(data.keys()) - {"status", "hours_played"}
    if unknown:
        errors = [{"field": f, "message": f"El campo '{f}' no está permitido."} for f in unknown]
        return error_400(errors)

    errors = []

    if "status" in data:
        if not isinstance(data["status"], str):
            errors.append({"field": "status", "message": "'status' debe ser un string."})
        elif data["status"] not in ALLOWED_STATUSES:
            errors.append({"field": "status", "message": f"'status' debe ser uno de: {', '.join(ALLOWED_STATUSES)}. Recibido: '{data['status']}'."})

    if "hours_played" in data:
        if not isinstance(data["hours_played"], int) or isinstance(data["hours_played"], bool):
            errors.append({"field": "hours_played", "message": "'hours_played' debe ser un integer."})
        elif data["hours_played"] < 0:
            errors.append({"field": "hours_played", "message": "'hours_played' debe ser >= 0."})

    if errors:
        return error_400(errors)

    if "status" in data:
        entry.status = data["status"]
    if "hours_played" in data:
        entry.hours_played = data["hours_played"]
    entry.save()

    return JsonResponse(
        {
            "id": entry.id,
            "external_game_id": entry.external_game_id,
            "status": entry.status,
            "hours_played": entry.hours_played,
        },
        status=200,
    )
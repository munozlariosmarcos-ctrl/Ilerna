import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .models import LibraryEntry


ALLOWED_STATUSES = LibraryEntry.ALLOWED_STATUSES


# ── health ───────────────────────────────────────────────────────────────────

@require_GET
def health(request):
    return JsonResponse({"status": "ok"})


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

def _error_401():
    return JsonResponse(
        {
            "error": "unauthorized",
            "message": "No autenticado",
        },
        status=401,
    )

def _error_404():
    return JsonResponse(
        {
            "error": "not_found",
            "message": "La entrada solicitada no existe",
        },
        status=404,
    )


def _validate_entry(data):
    errors = []

    if "external_game_id" not in data:
        errors.append({"field": "external_game_id", "message": "El campo 'external_game_id' es obligatorio."})
    elif not isinstance(data["external_game_id"], str) or not data["external_game_id"].strip():
        errors.append({"field": "external_game_id", "message": "'external_game_id' debe ser un string no vacío."})

    if "status" not in data:
        errors.append({"field": "status", "message": "El campo 'status' es obligatorio."})
    elif not isinstance(data["status"], str):
        errors.append({"field": "status", "message": "'status' debe ser un string."})
    elif data["status"] not in ALLOWED_STATUSES:
        errors.append({"field": "status", "message": f"'status' debe ser uno de: {', '.join(ALLOWED_STATUSES)}. Recibido: '{data['status']}'."})

    if "hours_played" not in data:
        errors.append({"field": "hours_played", "message": "El campo 'hours_played' es obligatorio."})
    elif not isinstance(data["hours_played"], int) or isinstance(data["hours_played"], bool):
        errors.append({"field": "hours_played", "message": "'hours_played' debe ser un integer."})
    elif data["hours_played"] < 0:
        errors.append({"field": "hours_played", "message": "'hours_played' debe ser >= 0."})

    return errors


# ── /api/library/entries/ ─────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["GET", "POST"])
def library_entries(request):

    # ← NUEVO: comprobar autenticación
    if not request.user.is_authenticated:
        return _error_401()

    if request.method == "GET":
        # ← NUEVO: filtrar solo las entradas del usuario autenticado
        entries = LibraryEntry.objects.filter(user=request.user)
        data = [
            {
                "id": e.id,
                "external_game_id": e.external_game_id,
                "status": e.status,
                "hours_played": e.hours_played,
            }
            for e in entries
        ]
        return JsonResponse(data, safe=False, status=200)

    # POST
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return _error_400([{"field": "body", "message": "El body debe ser un JSON válido."}])

    if not data:
        return _error_400([{"field": "body", "message": "El body no puede estar vacío. Se requieren: external_game_id, status, hours_played."}])

    errors = _validate_entry(data)
    if errors:
        return _error_400(errors)

    try:
        entry = LibraryEntry.objects.create(
            external_game_id=data["external_game_id"],
            status=data["status"],
            hours_played=data["hours_played"],
            user=request.user,  # ← NUEVO: asociar al usuario autenticado
        )
    except IntegrityError:
        return JsonResponse(
            {
                "error": "duplicate_entry",
                "message": "El juego ya existe en la biblioteca",
                "details": {"external_game_id": "duplicate"},
            },
            status=400,
        )

    return JsonResponse(
        {
            "id": entry.id,
            "external_game_id": entry.external_game_id,
            "status": entry.status,
            "hours_played": entry.hours_played,
        },
        status=201,
    )


# ── /api/library/entries/{id}/ ────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["GET", "PATCH"])
def library_entry_by_id(request, id):

    # ← NUEVO: comprobar autenticación
    if not request.user.is_authenticated:
        return _error_401()

    # ← NUEVO: buscar solo entre las entradas del usuario autenticado
    try:
        entry = LibraryEntry.objects.get(pk=id, user=request.user)
    except LibraryEntry.DoesNotExist:
        return _error_404()

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


    # PATCH
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return _error_400([{"field": "body", "message": "El body debe ser un JSON válido."}])

    if not data:
        return _error_400([{"field": "body", "message": "El body no puede estar vacío. Se requieren: status y/o hours_played."}])

    unknown = set(data.keys()) - {"status", "hours_played"}
    if unknown:
        errors = [{"field": f, "message": f"El campo '{f}' no está permitido."} for f in unknown]
        return _error_400(errors)

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
        return _error_400(errors)

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
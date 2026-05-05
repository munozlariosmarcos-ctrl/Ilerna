import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()

LOGIN_URL = "/api/auth/login/"
ENTRIES_URL = "/api/library/entries/"

class LibraryEntryExternalIdLengthTests(TestCase):
    def test_health(self):
        # Precondiciones

        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.get("/api/health/")

        # Comprobaciones
        # Comprobar el código HTTP que devuelve una vista
        self.assertEqual(response.status_code, 200)
        # Comprobar el contenido de la respuesta
        self.assertEqual(response.json(), {"status": "ok"})
        # Verifica que una clave existe dentro del JSON de la respuesta.
        self.assertIn("status", response.json())
        # Comprueba el valor concreto devuelto por la vista.
        self.assertEqual(response.json()["status"], "ok")
        # Asegura que la respuesta no contiene información que no debería aparecer.
        self.assertNotIn("paco", response.json())

        
class HealthCheckTests(TestCase):
    """
    Ejercicio 6 — Tests automáticos para la vista /api/health/
    """

    # ── Test principal ──────────────────────────────────────────────────────

    def test_health_returns_200(self):
        """El endpoint /api/health/ debe responder con HTTP 200."""
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)

    def test_health_returns_json_with_status_ok(self):
        """La respuesta debe ser un JSON con exactamente {"status": "ok"}."""
        response = self.client.get("/api/health/")
        data = response.json()
        self.assertEqual(data, {"status": "ok"})

    def test_health_json_contains_status_key(self):
        """El JSON de la respuesta debe contener la clave 'status'."""
        response = self.client.get("/api/health/")
        self.assertIn("status", response.json())

    def test_health_status_value_is_ok(self):
        """El valor de 'status' en el JSON debe ser exactamente 'ok'."""
        response = self.client.get("/api/health/")
        self.assertEqual(response.json()["status"], "ok")

    def test_health_json_has_no_extra_keys(self):
        """
        El JSON no debe contener claves inesperadas.
        Si alguien añade campos extra a la vista, este test fallará.
        """
        response = self.client.get("/api/health/")
        self.assertEqual(set(response.json().keys()), {"status"})

    # ── Tests que comprueban que el test FALLA si se altera la vista ────────

    def test_health_does_not_return_error_status(self):
        """
        El valor de 'status' no debe indicar un error.
        Si la vista cambia "ok" por "error", este test detecta la regresión.
        """
        response = self.client.get("/api/health/")
        self.assertNotEqual(response.json()["status"], "error")

    def test_health_does_not_return_404(self):
        """
        La ruta debe estar registrada.
        Un 404 indicaría que la URL fue eliminada o mal configurada.
        """
        response = self.client.get("/api/health/")
        self.assertNotEqual(response.status_code, 404)

    def test_health_does_not_return_500(self):
        """
        La vista no debe lanzar una excepción interna.
        Un 500 indicaría un error en el código de la vista.
        """
        response = self.client.get("/api/health/")
        self.assertNotEqual(response.status_code, 500)

    def test_health_content_type_is_json(self):
        """
        La respuesta debe tener Content-Type application/json.
        Si la vista deja de devolver JSON, este test lo detecta.
        """
        response = self.client.get("/api/health/")
        self.assertIn("application/json", response["Content-Type"])


class HealthCheckTests(TestCase):
    """
    Ejercicio 6 — Tests automáticos para la vista /api/health/
    """

    # ── Test principal ──────────────────────────────────────────────────────

    def test_health_returns_200(self):
        """El endpoint /api/health/ debe responder con HTTP 200."""
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)

    def test_health_returns_json_with_status_ok(self):
        """La respuesta debe ser un JSON con exactamente {"status": "ok"}."""
        response = self.client.get("/api/health/")
        data = response.json()
        self.assertEqual(data, {"status": "ok"})

    def test_health_json_contains_status_key(self):
        """El JSON de la respuesta debe contener la clave 'status'."""
        response = self.client.get("/api/health/")
        self.assertIn("status", response.json())

    def test_health_status_value_is_ok(self):
        """El valor de 'status' en el JSON debe ser exactamente 'ok'."""
        response = self.client.get("/api/health/")
        self.assertEqual(response.json()["status"], "ok")

    def test_health_json_has_no_extra_keys(self):
        """
        El JSON no debe contener claves inesperadas.
        Si alguien añade campos extra a la vista, este test fallará.
        """
        response = self.client.get("/api/health/")
        self.assertEqual(set(response.json().keys()), {"status"})

    # ── Tests que comprueban que el test FALLA si se altera la vista ────────

    def test_health_does_not_return_error_status(self):
        """
        El valor de 'status' no debe indicar un error.
        Si la vista cambia "ok" por "error", este test detecta la regresión.
        """
        response = self.client.get("/api/health/")
        self.assertNotEqual(response.json()["status"], "error")

    def test_health_does_not_return_404(self):
        """
        La ruta debe estar registrada.
        Un 404 indicaría que la URL fue eliminada o mal configurada.
        """
        response = self.client.get("/api/health/")
        self.assertNotEqual(response.status_code, 404)

    def test_health_does_not_return_500(self):
        """
        La vista no debe lanzar una excepción interna.
        Un 500 indicaría un error en el código de la vista.
        """
        response = self.client.get("/api/health/")
        self.assertNotEqual(response.status_code, 500)

    def test_health_content_type_is_json(self):
        """
        La respuesta debe tener Content-Type application/json.
        Si la vista deja de devolver JSON, este test lo detecta.
        """
        response = self.client.get("/api/health/")
        self.assertIn("application/json", response["Content-Type"])



ENTRIES_URL = "/api/library/entries/"


class LibraryEntriesAuthTests(TestCase):

    def setUp(self):
        """Crea dos usuarios de prueba antes de cada test."""
        self.ana = User.objects.create_user(username="ana", password="password123")
        self.carlos = User.objects.create_user(username="carlos", password="password123")

    def _login(self, username, password="password123"):
        """Helper para hacer login rápido."""
        self.client.post(   
            LOGIN_URL,
            data=json.dumps({"username": username, "password": password}),
            content_type="application/json",
        )

    # ── Sin autenticar ────────────────────────────────────────────────────────

    def test_entries_without_login_returns_401(self):
        """Sin autenticar debe devolver HTTP 401."""
        response = self.client.get(ENTRIES_URL)
        self.assertEqual(response.status_code, 401)

    def test_entries_without_login_returns_unauthorized(self):
        """Sin autenticar debe devolver error: unauthorized."""
        response = self.client.get(ENTRIES_URL)
        self.assertEqual(response.json()["error"], "unauthorized")

    def test_entries_without_login_returns_correct_message(self):
        """Sin autenticar el mensaje debe ser exactamente 'No autenticado'."""
        response = self.client.get(ENTRIES_URL)
        self.assertEqual(response.json()["message"], "No autenticado")

    # ── Autenticado ───────────────────────────────────────────────────────────

    def test_entries_with_login_returns_200(self):
        """Autenticado debe devolver HTTP 200."""
        self._login("ana")
        response = self.client.get(ENTRIES_URL)
        self.assertEqual(response.status_code, 200)

    def test_entries_with_login_returns_list(self):
        """Autenticado debe devolver una lista."""
        self._login("ana")
        response = self.client.get(ENTRIES_URL)
        self.assertIsInstance(response.json(), list)

    # ── Dos usuarios ven solo sus entradas ────────────────────────────────────

    def test_ana_only_sees_her_entries(self):
        """Ana solo debe ver sus propias entradas."""
        self._login("ana")
        self.client.post(
            ENTRIES_URL,
            data=json.dumps({
                "external_game_id": "juego-de-ana",
                "status": "playing",
                "hours_played": 5,
            }),
            content_type="application/json",
        )

        self._login("carlos")
        self.client.post(
            ENTRIES_URL,
            data=json.dumps({
                "external_game_id": "juego-de-carlos",
                "status": "wishlist",
                "hours_played": 0,
            }),
            content_type="application/json",
        )

        self._login("ana")
        response = self.client.get(ENTRIES_URL)
        ids = [e["external_game_id"] for e in response.json()]
        self.assertIn("juego-de-ana", ids)
        self.assertNotIn("juego-de-carlos", ids)

    def test_carlos_only_sees_his_entries(self):
        """Carlos solo debe ver sus propias entradas."""
        self._login("ana")
        self.client.post(
            ENTRIES_URL,
            data=json.dumps({
                "external_game_id": "juego-de-ana",
                "status": "playing",
                "hours_played": 5,
            }),
            content_type="application/json",
        )

        self._login("carlos")
        self.client.post(
            ENTRIES_URL,
            data=json.dumps({
                "external_game_id": "juego-de-carlos",
                "status": "wishlist",
                "hours_played": 0,
            }),
            content_type="application/json",
        )

        response = self.client.get(ENTRIES_URL)
        ids = [e["external_game_id"] for e in response.json()]
        self.assertIn("juego-de-carlos", ids)
        self.assertNotIn("juego-de-ana", ids)

    def test_entries_count_matches_user(self):
        """El número de entradas devueltas debe coincidir con las del usuario."""
        self._login("ana")
        self.client.post(
            ENTRIES_URL,
            data=json.dumps({
                "external_game_id": "juego-de-ana",
                "status": "playing",
                "hours_played": 5,
            }),
            content_type="application/json",
        )
        response = self.client.get(ENTRIES_URL)
        self.assertEqual(len(response.json()), 1)


class LibraryEntryDetailAuthTests(TestCase):

    def _login(self, username, password="password123"):
        """Helper para hacer login rápido."""
        self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": username, "password": password}),
            content_type="application/json",
        )

    def setUp(self):
        """Crea dos usuarios y una entrada para cada uno."""
        self.ana = User.objects.create_user(username="ana", password="password123")
        self.carlos = User.objects.create_user(username="carlos", password="password123")

        self._login("ana")
        response = self.client.post(
            ENTRIES_URL,
            data=json.dumps({
                "external_game_id": "juego-de-ana",
                "status": "playing",
                "hours_played": 5,
            }),
            content_type="application/json",
        )
        self.ana_entry_id = response.json()["id"]

        self._login("carlos")
        response = self.client.post(
            ENTRIES_URL,
            data=json.dumps({
                "external_game_id": "juego-de-carlos",
                "status": "wishlist",
                "hours_played": 0,
            }),
            content_type="application/json",
        )
        self.carlos_entry_id = response.json()["id"]

        self.client.logout()



    # ── Sin autenticar ────────────────────────────────────────────────────────

    def test_detail_without_login_returns_401(self):
        """Sin autenticar debe devolver HTTP 401."""
        response = self.client.get(f"{ENTRIES_URL}{self.ana_entry_id}/")
        self.assertEqual(response.status_code, 401)

    def test_detail_without_login_returns_unauthorized(self):
        """Sin autenticar debe devolver error: unauthorized."""
        response = self.client.get(f"{ENTRIES_URL}{self.ana_entry_id}/")
        self.assertEqual(response.json()["error"], "unauthorized")

    def test_detail_without_login_returns_correct_message(self):
        """Sin autenticar el mensaje debe ser exactamente 'No autenticado'."""
        response = self.client.get(f"{ENTRIES_URL}{self.ana_entry_id}/")
        self.assertEqual(response.json()["message"], "No autenticado")

    # ── Autenticado y entrada propia ──────────────────────────────────────────

    def test_detail_own_entry_returns_200(self):
        """Autenticado y entrada propia debe devolver HTTP 200."""
        self._login("ana")
        response = self.client.get(f"{ENTRIES_URL}{self.ana_entry_id}/")
        self.assertEqual(response.status_code, 200)

    def test_detail_own_entry_returns_correct_data(self):
        """Autenticado debe devolver los datos de la entrada."""
        self._login("ana")
        response = self.client.get(f"{ENTRIES_URL}{self.ana_entry_id}/")
        data = response.json()
        self.assertEqual(data["external_game_id"], "juego-de-ana")
        self.assertEqual(data["status"], "playing")
        self.assertEqual(data["hours_played"], 5)

    def test_detail_own_entry_returns_id(self):
        """La respuesta debe contener el id de la entrada."""
        self._login("ana")
        response = self.client.get(f"{ENTRIES_URL}{self.ana_entry_id}/")
        self.assertIn("id", response.json())

    # ── Autenticado y entrada de otro usuario ─────────────────────────────────

    def test_detail_other_user_entry_returns_404(self):
        """Acceder a la entrada de otro usuario debe devolver HTTP 404."""
        self._login("carlos")
        response = self.client.get(f"{ENTRIES_URL}{self.ana_entry_id}/")
        self.assertEqual(response.status_code, 404)

    def test_detail_other_user_entry_returns_not_found(self):
        """Acceder a la entrada de otro usuario debe devolver error: not_found."""
        self._login("carlos")
        response = self.client.get(f"{ENTRIES_URL}{self.ana_entry_id}/")
        self.assertEqual(response.json()["error"], "not_found")

    def test_detail_other_user_entry_returns_correct_message(self):
        """El mensaje debe ser exactamente 'La entrada solicitada no existe'."""
        self._login("carlos")
        response = self.client.get(f"{ENTRIES_URL}{self.ana_entry_id}/")
        self.assertEqual(response.json()["message"], "La entrada solicitada no existe")

    def test_detail_other_user_entry_does_not_reveal_existence(self):
        """Un 404 no debe revelar que la entrada existe pero es de otro usuario."""
        self._login("carlos")
        response_other = self.client.get(f"{ENTRIES_URL}{self.ana_entry_id}/")
        response_nonexistent = self.client.get(f"{ENTRIES_URL}99999/")
        # Ambos deben devolver exactamente el mismo error
        self.assertEqual(response_other.json(), response_nonexistent.json())    


class LibraryEntriesCreateAuthTests(TestCase):

    def setUp(self):
        """Crea dos usuarios de prueba antes de cada test."""
        self.ana = User.objects.create_user(username="ana", password="password123")
        self.carlos = User.objects.create_user(username="carlos", password="password123")

    def _login(self, username, password="password123"):
        """Helper para hacer login rápido."""
        self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": username, "password": password}),
            content_type="application/json",
        )

    # ── Sin autenticar ────────────────────────────────────────────────────────

    def test_create_without_login_returns_401(self):
        """Sin autenticar debe devolver HTTP 401."""
        response = self.client.post(
            ENTRIES_URL,
            data=json.dumps({
                "external_game_id": "juego-1",
                "status": "playing",
                "hours_played": 5,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_create_without_login_returns_unauthorized(self):
        """Sin autenticar debe devolver error: unauthorized."""
        response = self.client.post(
            ENTRIES_URL,
            data=json.dumps({
                "external_game_id": "juego-1",
                "status": "playing",
                "hours_played": 5,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.json()["error"], "unauthorized")

    def test_create_without_login_returns_correct_message(self):
        """Sin autenticar el mensaje debe ser exactamente 'No autenticado'."""
        response = self.client.post(
            ENTRIES_URL,
            data=json.dumps({
                "external_game_id": "juego-1",
                "status": "playing",
                "hours_played": 5,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.json()["message"], "No autenticado")

    # ── Autenticado ───────────────────────────────────────────────────────────

    def test_create_authenticated_returns_201(self):
        """Autenticado debe devolver HTTP 201."""
        self._login("ana")
        response = self.client.post(
            ENTRIES_URL,
            data=json.dumps({
                "external_game_id": "juego-de-ana",
                "status": "playing",
                "hours_played": 5,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_create_authenticated_returns_correct_data(self):
        """La respuesta debe contener los datos de la entrada creada."""
        self._login("ana")
        response = self.client.post(
            ENTRIES_URL,
            data=json.dumps({
                "external_game_id": "juego-de-ana",
                "status": "playing",
                "hours_played": 5,
            }),
            content_type="application/json",
        )
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["external_game_id"], "juego-de-ana")
        self.assertEqual(data["status"], "playing")
        self.assertEqual(data["hours_played"], 5)

    # ── Aislamiento ───────────────────────────────────────────────────────────

    def test_create_entry_not_visible_to_other_user(self):
        """Una entrada creada por ana no debe aparecer en el listado de carlos."""
        self._login("ana")
        self.client.post(
            ENTRIES_URL,
            data=json.dumps({
                "external_game_id": "juego-de-ana",
                "status": "playing",
                "hours_played": 5,
            }),
            content_type="application/json",
        )

        self._login("carlos")
        response = self.client.get(ENTRIES_URL)
        ids = [e["external_game_id"] for e in response.json()]
        self.assertNotIn("juego-de-ana", ids)

    def test_create_entry_visible_to_owner(self):
        """Una entrada creada por ana debe aparecer en su propio listado."""
        self._login("ana")
        self.client.post(
            ENTRIES_URL,
            data=json.dumps({
                "external_game_id": "juego-de-ana",
                "status": "playing",
                "hours_played": 5,
            }),
            content_type="application/json",
        )

        response = self.client.get(ENTRIES_URL)
        ids = [e["external_game_id"] for e in response.json()]
        self.assertIn("juego-de-ana", ids)

    def test_create_entry_associated_to_authenticated_user(self):
        """La entrada creada debe quedar asociada al usuario autenticado."""
        self._login("ana")
        response = self.client.post(
            ENTRIES_URL,
            data=json.dumps({
                "external_game_id": "juego-de-ana",
                "status": "playing",
                "hours_played": 5,
            }),
            content_type="application/json",
        )
        entry_id = response.json()["id"]

        # Ana puede acceder a su entrada
        response = self.client.get(f"{ENTRIES_URL}{entry_id}/")
        self.assertEqual(response.status_code, 200)

        # Carlos no puede acceder a la entrada de ana
        self._login("carlos")
        response = self.client.get(f"{ENTRIES_URL}{entry_id}/")
        self.assertEqual(response.status_code, 404)
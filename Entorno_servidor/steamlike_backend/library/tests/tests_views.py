from django.test import TestCase

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


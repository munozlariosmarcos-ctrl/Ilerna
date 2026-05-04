from django.test import TestCase
import json
from django.contrib.auth import get_user_model

User = get_user_model()

REGISTER_URL = "/api/auth/register/"
LOGIN_URL = "/api/auth/login/"
ME_URL = "/api/users/me/"


class RegisterViewTests(TestCase):

    # ── Caso válido ───────────────────────────────────────────────────────────

    def test_register_valid_returns_201(self):
        """Un registro correcto debe devolver HTTP 201."""
        response = self.client.post(
            REGISTER_URL,
            data=json.dumps({"username": "ana", "password": "password123", "email": "ana@ejemplo.com"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_register_valid_returns_id_and_username(self):
        """La respuesta debe contener id y username."""
        response = self.client.post(
            REGISTER_URL,
            data=json.dumps({"username": "ana", "password": "password123", "email": "ana@ejemplo.com"}),
            content_type="application/json",
        )
        data = response.json()
        self.assertIn("id", data)
        self.assertIn("username", data)
        self.assertEqual(data["username"], "ana")

    def test_register_valid_does_not_return_password(self):
        """La respuesta NO debe contener la contraseña."""
        response = self.client.post(
            REGISTER_URL,
            data=json.dumps({"username": "ana", "password": "password123", "email": "ana@ejemplo.com"}),
            content_type="application/json",
        )
        self.assertNotIn("password", response.json())

    def test_register_creates_user_in_database(self):
        """El usuario debe quedar guardado en la base de datos."""
        self.client.post(
            REGISTER_URL,
            data=json.dumps({"username": "ana", "password": "password123", "email": "ana@ejemplo.com"}),
            content_type="application/json",
        )
        self.assertTrue(User.objects.filter(username="ana").exists())

    # ── JSON vacío ────────────────────────────────────────────────────────────

    def test_register_empty_json_returns_400(self):
        """Un JSON vacío debe devolver HTTP 400."""
        response = self.client.post(
            REGISTER_URL,
            data=json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_register_empty_json_returns_validation_error(self):
        """Un JSON vacío debe devolver error: validation_error."""
        response = self.client.post(
            REGISTER_URL,
            data=json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.json()["error"], "validation_error")

    # ── Campos ausentes ───────────────────────────────────────────────────────

    def test_register_missing_password_returns_400(self):
        """Si falta password debe devolver HTTP 400."""
        response = self.client.post(
            REGISTER_URL,
            data=json.dumps({"username": "ana", "email": "ana@ejemplo.com"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_register_missing_username_returns_400(self):
        """Si falta username debe devolver HTTP 400."""
        response = self.client.post(
            REGISTER_URL,
            data=json.dumps({"password": "password123", "email": "ana@ejemplo.com"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_register_missing_fields_returns_validation_error(self):
        """Si faltan campos debe devolver error: validation_error."""
        response = self.client.post(
            REGISTER_URL,
            data=json.dumps({"username": "ana", "email": "ana@ejemplo.com"}),
            content_type="application/json",
        )
        self.assertEqual(response.json()["error"], "validation_error")

    # ── Contraseña corta ──────────────────────────────────────────────────────

    def test_register_short_password_returns_400(self):
        """Una password menor de 8 caracteres debe devolver HTTP 400."""
        response = self.client.post(
            REGISTER_URL,
            data=json.dumps({"username": "ana", "password": "abc", "email": "ana@ejemplo.com"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_register_short_password_returns_validation_error(self):
        """Una password corta debe devolver error: validation_error."""
        response = self.client.post(
            REGISTER_URL,
            data=json.dumps({"username": "ana", "password": "abc", "email": "ana@ejemplo.com"}),
            content_type="application/json",
        )
        self.assertEqual(response.json()["error"], "validation_error")

    def test_register_short_password_error_in_details(self):
        """El campo password debe aparecer en details del error."""
        response = self.client.post(
            REGISTER_URL,
            data=json.dumps({"username": "ana", "password": "abc", "email": "ana@ejemplo.com"}),
            content_type="application/json",
        )
        self.assertIn("password", response.json()["details"])

    # ── Username repetido ─────────────────────────────────────────────────────

    def test_register_duplicate_username_returns_400(self):
        """Un username ya en uso debe devolver HTTP 400."""
        User.objects.create_user(username="ana", password="password123", email="ana@ejemplo.com")
        response = self.client.post(
            REGISTER_URL,
            data=json.dumps({"username": "ana", "password": "otrapassword123", "email": "ana2@ejemplo.com"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_register_duplicate_username_returns_validation_error(self):
        """Un username repetido debe devolver error: validation_error."""
        User.objects.create_user(username="ana", password="password123", email="ana@ejemplo.com")
        response = self.client.post(
            REGISTER_URL,
            data=json.dumps({"username": "ana", "password": "otrapassword123", "email": "ana2@ejemplo.com"}),
            content_type="application/json",
        )
        self.assertEqual(response.json()["error"], "validation_error")

    def test_register_duplicate_username_error_in_details(self):
        """El campo username debe aparecer en details del error."""
        User.objects.create_user(username="ana", password="password123", email="ana@ejemplo.com")
        response = self.client.post(
            REGISTER_URL,
            data=json.dumps({"username": "ana", "password": "otrapassword123", "email": "ana2@ejemplo.com"}),
            content_type="application/json",
        )
        self.assertIn("username", response.json()["details"])


class LoginViewTests(TestCase):

    def setUp(self):
        """Crea un usuario de prueba antes de cada test."""
        User.objects.create_user(username="ana", password="password123", email="ana@ejemplo.com")

    # ── Caso válido ───────────────────────────────────────────────────────────

    def test_login_valid_returns_200(self):
        """Un login correcto debe devolver HTTP 200."""
        response = self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": "ana", "password": "password123"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_login_valid_returns_id_and_username(self):
        """La respuesta debe contener id y username."""
        response = self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": "ana", "password": "password123"}),
            content_type="application/json",
        )
        data = response.json()
        self.assertIn("id", data)
        self.assertIn("username", data)
        self.assertEqual(data["username"], "ana")

    def test_login_valid_does_not_return_password(self):
        """La respuesta NO debe contener la contraseña."""
        response = self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": "ana", "password": "password123"}),
            content_type="application/json",
        )
        self.assertNotIn("password", response.json())

    # ── Credenciales incorrectas ──────────────────────────────────────────────

    def test_login_wrong_password_returns_401(self):
        """Una password incorrecta debe devolver HTTP 401."""
        response = self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": "ana", "password": "wrongpassword"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_login_wrong_password_returns_unauthorized(self):
        """Una password incorrecta debe devolver error: unauthorized."""
        response = self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": "ana", "password": "wrongpassword"}),
            content_type="application/json",
        )
        self.assertEqual(response.json()["error"], "unauthorized")

    def test_login_wrong_password_returns_correct_message(self):
        """El mensaje debe ser exactamente 'Credenciales incorrectas'."""
        response = self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": "ana", "password": "wrongpassword"}),
            content_type="application/json",
        )
        self.assertEqual(response.json()["message"], "Credenciales incorrectas")

    def test_login_wrong_username_returns_401(self):
        """Un username que no existe debe devolver HTTP 401."""
        response = self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": "noexiste", "password": "password123"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    # ── Validación — campos ausentes ──────────────────────────────────────────

    def test_login_missing_password_returns_400(self):
        """Si falta password debe devolver HTTP 400."""
        response = self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": "ana"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_login_missing_username_returns_400(self):
        """Si falta username debe devolver HTTP 400."""
        response = self.client.post(
            LOGIN_URL,
            data=json.dumps({"password": "password123"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_login_missing_fields_returns_validation_error(self):
        """Si faltan campos debe devolver error: validation_error."""
        response = self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": "ana"}),
            content_type="application/json",
        )
        self.assertEqual(response.json()["error"], "validation_error")

    # ── Validación — JSON vacío ───────────────────────────────────────────────

    def test_login_empty_json_returns_400(self):
        """Un JSON vacío debe devolver HTTP 400."""
        response = self.client.post(
            LOGIN_URL,
            data=json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_login_empty_json_returns_validation_error(self):
        """Un JSON vacío debe devolver error: validation_error."""
        response = self.client.post(
            LOGIN_URL,
            data=json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.json()["error"], "validation_error")

    # ── Validación — tipos incorrectos ────────────────────────────────────────

    def test_login_invalid_type_username_returns_400(self):
        """Si username no es string debe devolver HTTP 400."""
        response = self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": 12345, "password": "password123"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_login_invalid_type_returns_validation_error(self):
        """Si los tipos son incorrectos debe devolver error: validation_error."""
        response = self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": 12345, "password": "password123"}),
            content_type="application/json",
        )
        self.assertEqual(response.json()["error"], "validation_error")


class MeViewTests(TestCase):

    def setUp(self):
        """Crea un usuario de prueba antes de cada test."""
        User.objects.create_user(username="ana", password="password123", email="ana@ejemplo.com")

    # ── Sin autenticar ────────────────────────────────────────────────────────

    def test_me_without_login_returns_401(self):
        """Sin autenticar debe devolver HTTP 401."""
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, 401)

    def test_me_without_login_returns_unauthorized(self):
        """Sin autenticar debe devolver error: unauthorized."""
        response = self.client.get(ME_URL)
        self.assertEqual(response.json()["error"], "unauthorized")

    def test_me_without_login_returns_correct_message(self):
        """Sin autenticar el mensaje debe ser exactamente 'No autenticado'."""
        response = self.client.get(ME_URL)
        self.assertEqual(response.json()["message"], "No autenticado")

    def test_me_without_login_does_not_return_200(self):
        """Sin autenticar no debe devolver HTTP 200."""
        response = self.client.get(ME_URL)
        self.assertNotEqual(response.status_code, 200)

    # ── Tras login correcto ───────────────────────────────────────────────────

    def test_me_after_login_returns_200(self):
        """Tras login correcto debe devolver HTTP 200."""
        self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": "ana", "password": "password123"}),
            content_type="application/json",
        )
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, 200)

    def test_me_after_login_returns_id_and_username(self):
        """Tras login correcto debe devolver id y username."""
        self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": "ana", "password": "password123"}),
            content_type="application/json",
        )
        response = self.client.get(ME_URL)
        data = response.json()
        self.assertIn("id", data)
        self.assertIn("username", data)
        self.assertEqual(data["username"], "ana")

    def test_me_after_login_does_not_return_password(self):
        """Tras login correcto la respuesta NO debe contener la contraseña."""
        self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": "ana", "password": "password123"}),
            content_type="application/json",
        )
        response = self.client.get(ME_URL)
        self.assertNotIn("password", response.json())

    def test_me_after_login_returns_correct_user(self):
        """Tras login debe devolver los datos del usuario autenticado."""
        self.client.post(
            LOGIN_URL,
            data=json.dumps({"username": "ana", "password": "password123"}),
            content_type="application/json",
        )
        response = self.client.get(ME_URL)
        self.assertEqual(response.json()["username"], "ana")
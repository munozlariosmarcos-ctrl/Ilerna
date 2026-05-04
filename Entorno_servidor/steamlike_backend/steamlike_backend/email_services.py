import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class EmailServiceError(Exception):
    def __init__(self, error, message, status):
        self.error = error
        self.message = message
        self.status = status
        super().__init__(message)


def send_email(to, subject, text, html=None, action="send_email", user=None):
    """
    Envía un email usando Maileroo.

    Args:
        to: Email destinatario
        subject: Asunto
        text: Cuerpo en texto plano
        html: Cuerpo en HTML (opcional)
        action: Nombre de la acción para el log (send_email, register_welcome...)
        user: Usuario que dispara el envío (opcional)
    """
    api_key = settings.MAILEROO_API_KEY
    from_address = settings.MAILEROO_FROM

    # Contexto para los logs
    context = {
        "action": action,
        "to": to,
        "subject": subject,
    }
    if user:
        context["user_id"] = getattr(user, "id", None)
        context["username"] = getattr(user, "username", None)

    # Log de intento
    logger.info("Intento de envío de email | action=%(action)s to=%(to)s subject=%(subject)s", context)

    payload = {
        'from': from_address,
        'to': to,
        'subject': subject,
        'plain': text,
    }
    if html:
        payload['html'] = html

    # Caso A — timeout o error de red → 503
    try:
        response = requests.post(
            'https://smtp.maileroo.com/send',
            headers={
                'X-API-Key': api_key,
            },
            data=payload,
            timeout=5,
        )
    except requests.Timeout:
        logger.error(
            "Fallo por timeout al enviar email | action=%(action)s to=%(to)s",
            context,
        )
        raise EmailServiceError('external_service_unavailable', 'El servicio de email no está disponible.', 503)
    except requests.ConnectionError:
        logger.error(
            "Fallo por error de red al enviar email | action=%(action)s to=%(to)s",
            context,
        )
        raise EmailServiceError('external_service_unavailable', 'El servicio de email no está disponible.', 503)

    # Caso B — respuesta con error → 502
    if not response.ok:
        logger.error(
            "Fallo por respuesta del proveedor | action=%(action)s to=%(to)s status_code=%(status_code)s",
            {**context, "status_code": response.status_code},
        )
        raise EmailServiceError('external_service_error', 'Error al enviar el email.', 502)

    try:
        data = response.json()
        if not data:
            raise ValueError('Respuesta vacía')
    except Exception:
        logger.error(
            "Fallo por respuesta inválida del proveedor | action=%(action)s to=%(to)s",
            context,
        )
        raise EmailServiceError('external_service_error', 'Error al enviar el email.', 502)

    # Log de éxito
    logger.info(
        "Email enviado correctamente | action=%(action)s to=%(to)s result=ok",
        context,
    )

    return data
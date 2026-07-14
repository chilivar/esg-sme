import requests
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

from portal.utils.exeptions import EmailSendingException


def send_confirmation_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)

    host = settings.FRONT_URL
    scheme = "https" if request.is_secure() else "http"

    link = f"{scheme}://{host}/portal/confirm-email/{uid}/{token}/"

    email_sender_url = (
        f'{settings.EMAIL_SENDER_SERVICE_URL}'
        f'api/messages/registration'
    )

    try:
        payload = {
            "email": user.email,
            "link": link,
            "username": user.username,
        }

        response = requests.post(
            email_sender_url,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        return link

    except requests.RequestException as exc:
        raise EmailSendingException(
            f"Failed to send activation email: {exc}"
        ) from exc

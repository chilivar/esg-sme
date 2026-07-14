from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
import requests

from portal.utils.exeptions import EmailSendingException


def reset_password_request(request, data):
    email = data.get("email")

    user = User.objects.filter(
        email=email,
        is_active=True
    ).first()

    if not user:
        return

    uid = urlsafe_base64_encode(
        force_bytes(user.pk)
    )

    token = default_token_generator.make_token(user)

    host = settings.FRONT_URL
    scheme = "https" if request.is_secure() else "http"

    link = (
        f"{scheme}://{host}/portal/reset-password/{uid}/{token}/"
    )

    email_sender_url = (
        f'{settings.EMAIL_SENDER_SERVICE_URL}'
        f'api/messages/password-reset'
    )

    try:
        payload = {
            "email": user.email,
            "link": link,
            "username": user.username,
        }

        requests.post(
            email_sender_url,
            json=payload,
            timeout=60,
        )

        return link

    except requests.RequestException as exc:
        raise EmailSendingException(
            f"Failed to send activation email: {exc}"
        ) from exc

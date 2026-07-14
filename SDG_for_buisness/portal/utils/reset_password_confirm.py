from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import (
    default_token_generator
)
from portal.models import User
from portal.utils.exeptions import InvalidTokenException


def reset_password_confirm(data, uid, token):
    password = data["password"]

    try:
        user_id = (
            urlsafe_base64_decode(uid)
            .decode()
        )

        user = User.objects.get(
            id=user_id
        )

    except Exception:
        raise InvalidTokenException()

    if not default_token_generator.check_token(
        user,
        token
    ):
        raise InvalidTokenException()

    user.set_password(password)
    user.save()

    return user

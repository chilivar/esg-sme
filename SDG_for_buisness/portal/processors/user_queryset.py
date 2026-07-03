from django.db import transaction

from portal.models import User, Organization
from .model_interface import ModelInterface
from ..utils.exeptions import UserExistsException


class UserQuerySet(ModelInterface):
    def get_data(self):
        return User.objects.all()

    @transaction.atomic
    def post_data(self, data, **kwargs):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        user = User.objects.filter(username=username).first()
        if user:

            if user.is_active:
                raise UserExistsException("Username already exists")

            user.email = email
            user.set_password(password)
            user.save()

            user.email = email
            user.save(update_fields=["email"])
            Organization.objects.filter(user=user).update(
                email=email
            )

            return user

        user = User.objects.filter(email=email, is_active=True).first()
        if user:
            raise UserExistsException("Email already exists")

        user = User.objects.create_user(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            is_active=False,
        )

        organization = Organization.objects.create(user=user, email=data.get('email'))

        return user

    def patch_password(self, data, username):
        password = data.get("password")
        user = User.objects.get(username=username)

        user.set_password(password)
        user.save()

        return user
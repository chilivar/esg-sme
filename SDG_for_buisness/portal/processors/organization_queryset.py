from .model_interface import ModelInterface
from portal.models import User, Organization
from portal.model_serializer.organization_serializer import OrganizationSerializer


class OrganizationQuerySet(ModelInterface):

    def get_data(self, **kwargs):
        user = kwargs.get("user")
        org = Organization.objects.filter(user=user).values('id', 'organization_name', 'type', 'phone', 'email', 'city')

        return org

    def post_data(self, data, **kwargs):
        pass

    def put_data(self, data, **kwargs):
        user = kwargs.get("user")

        org = Organization.objects.get(user=user)

        serializer = OrganizationSerializer(
            org,
            data=data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer.data

    def get_settings_data(self, **kwargs):
        user = kwargs.get("user")
        settings = Organization.objects.filter(user=user).values('mailing').first()

        return settings

    def patch_data(self, data, **kwargs):
        user = kwargs.get("user")
        org = Organization.objects.get(user=user)

        allowed_fields = {"mailing"}  # whitelist

        for key, value in data.items():
            if key in allowed_fields:
                setattr(org, key, value)

        org.save()
        return org

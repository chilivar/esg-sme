from rest_framework.authentication import BaseAuthentication
from service_auth.models import ServiceClient
from rest_framework.exceptions import AuthenticationFailed


class ServiceAPIKeyAuthentication(BaseAuthentication):
    keyword = "X-API-KEY"

    def authenticate(self, request):
        key = request.headers.get(self.keyword)

        if not key:
            return None

        try:
            service = ServiceClient.objects.get(api_key=key, is_active=True)
        except ServiceClient.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")

        return (service, None)


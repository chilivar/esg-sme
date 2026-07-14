from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from service_auth.permissions import HasScope
from service_auth.authentication.service_api_key import ServiceAPIKeyAuthentication
from service_api.processors.mailing_users import MailingUsers

class MailingListAPIView(APIView):
    permission_classes = [IsAuthenticated, HasScope]
    authentication_classes = [ServiceAPIKeyAuthentication]

    required_scope = "mailing.read"
    def get(self, request):
        data = MailingUsers().get_data(user=request.user)

        return Response(data, status=200)

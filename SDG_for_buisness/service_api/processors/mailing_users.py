from portal.processors.model_interface import ModelInterface
from portal.models import Organization


class MailingUsers(ModelInterface):
    def get_data(self, **kwargs):
        org = Organization.objects.filter(mailing=True).values_list('email', flat=True)

        return list(org)

    def post_data(self, data, **kwargs):
        pass
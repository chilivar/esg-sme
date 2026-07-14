import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SDG_for_buisness.settings')

application = get_asgi_application()

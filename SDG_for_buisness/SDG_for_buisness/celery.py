import os

from celery import Celery


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'SDG_for_buisness.settings'
)

app = Celery('SDG_for_buisness')

app.config_from_object(
    'django.conf:settings',
    namespace='CELERY'
)

app.autodiscover_tasks()


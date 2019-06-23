import logging
import os

from celery import Celery

log = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snommoc.settings')

app = Celery('snommoc')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

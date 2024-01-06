import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog1.settings")
app = Celery("blog1")
app.conf.broker_connection_retry = True
app.conf.broker_connection_retry_on_startup = True
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
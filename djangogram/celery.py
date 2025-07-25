# djangogram/celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangogram.settings')

app = Celery('djangogram')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

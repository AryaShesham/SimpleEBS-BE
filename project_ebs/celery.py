
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_ebs.settings')

app = Celery('project_ebs')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Use Redis as the message broker
app.conf.broker_url = 'redis://localhost:6379/0'

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
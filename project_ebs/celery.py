from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_ebs.settings')

# Create a Celery instance named 'project_ebs'
app = Celery('project_ebs')

# Configure Celery from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Use Redis as the message broker
app.conf.broker_url = 'redis://localhost:6379/0'

# Automatically discover and register tasks from installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
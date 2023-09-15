#!/usr/bin/env python

import os
from celery import Celery
from django.conf import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')

app = Celery('portal')

# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')
app.conf['BROKER_URL'] = app.conf['CELERY_BROKER_URL']
app.conf['RESULT_BACKEND'] = app.conf['CELERY_RESULT_BACKEND']

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Set scheduled tasks
if settings.CELERY_BEAT_SCHEDULE is not None:
    app.conf.beat_schedule = settings.CELERY_BEAT_SCHEDULE
    app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

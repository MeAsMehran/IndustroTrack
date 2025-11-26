import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IndustroTrack.settings')

app = Celery('IndustroTrack')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periodic Tasks
app.conf.beat_schedule = {
    'fetch-device-data-every-10-seconds': {
        'task': 'machine.tasks.fetch_device_data',
        'schedule': 20.0,
    },
}

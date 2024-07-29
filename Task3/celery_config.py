from celery import Celery
from app.core.config import settings

app = Celery('tasks', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

app.conf.beat_schedule = {
    'update-data-every-hour': {
        'task': 'tasks.update_data.update_data',
        'schedule': 3600.0,
    },
}

app.autodiscover_tasks(['tasks'])

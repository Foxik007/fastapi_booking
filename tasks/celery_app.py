from celery import Celery
from celery.schedules import crontab

from config import settings

celery = Celery(
    'tasks',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
    include=['tasks.tasks',
             'tasks.scheduled'],
    broker_connection_retry_on_startup = True
)

celery.conf.beat_schedule = {
    'luboe_nazvanie': {
        'task':'periodic_task',
        'schedule':10, # секунды
        # 'schedule': crontab(minute='30',hour='15'),
    }
}
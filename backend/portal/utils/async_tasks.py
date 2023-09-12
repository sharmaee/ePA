import logging

from django.conf import settings
from redis import Redis
from portal.celery import app as celery_app


logger = logging.getLogger(__name__)
_background_tasks_supported = None


def background_tasks_supported():
    global _background_tasks_supported

    if _background_tasks_supported is not None:
        return _background_tasks_supported

    _background_tasks_supported = False
    r = Redis(settings.REDIS_HOST, socket_connect_timeout=1)
    try:
        r.ping()
    except Exception as e:
        logger.info(f"Redis server is unavailable: {e}")

    try:
        if celery_app.control.ping():
            _background_tasks_supported = True
        else:
            logger.info("Celery worker is not running")
    except Exception as e:
        logger.info(f"Celery is not running: {e}")


def try_run_in_background(task, args, expires):
    if background_tasks_supported():
        task.apply_async(args=args, expires=expires)

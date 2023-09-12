import os


CELERY_IMPORTS = ("portal",)
CELERY_BROKER_USE_SSL = None
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379")

CELERY_BEAT_SCHEDULE = {}

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")

worker_send_task_event = False
task_ignore_result = True

# task messages will be acknowledged after the task has been executed, not just before (the default behavior).
task_acks_late = True

# One worker taks 10 tasks from queue at a time and will increase the performance
worker_prefetch_multiplier = 10

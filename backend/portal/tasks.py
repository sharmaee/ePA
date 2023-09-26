import portal.utils.send_emails as email_handler
import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task()
def send_notification_task(notification_type, *args):
    email_handler.send_notification(notification_type, *args)

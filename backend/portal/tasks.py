from celery import shared_task
from portal.utils.send_emails import (
    send_new_request_notification,
    send_denial_notification,
    send_password_reset_email,
    send_activation_email,
    send_not_registered_promo_email,
    send_ran_out_of_seats,
)

import logging

logger = logging.getLogger(__name__)


@shared_task()
def send_new_request_notification_task():
    send_new_request_notification()


@shared_task()
def send_denial_notification_task():
    send_denial_notification()


@shared_task()
def send_password_reset_email_task():
    send_password_reset_email()


@shared_task()
def send_activation_email_task():
    send_activation_email()


@shared_task()
def send_not_registered_promo_email_task():
    send_not_registered_promo_email()


@shared_task()
def send_ran_out_of_seats_task():
    send_ran_out_of_seats()

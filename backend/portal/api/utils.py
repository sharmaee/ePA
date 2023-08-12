from typing import Any

from rest_framework import views
from portal.exceptions import PortalException
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> views.Response:
    """Custom API exception handler."""

    adapted_esc = PortalException.adapt_to_common_format(exc)

    # get the standard error response
    return views.exception_handler(adapted_esc, context)


def send_new_request_notification(requirements_request):
    subject = "Request for New Prior Auth Requirements"
    message = f"""
    DoPriorAuth user requested new prior auth requirements.\n\n
    Medication: {requirements_request.medication}\n
    Insurance Provider: {requirements_request.insurance_provider}\n
    Insurance Plan Type: {requirements_request.insurance_plan_type}\n
    Insurance Coverage State: {requirements_request.insurance_coverage_state}\n
    App Release Version: {requirements_request.release_version}\n
    Submission Date: {requirements_request.submission_date}\n
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_TO_EMAIL], fail_silently=False)
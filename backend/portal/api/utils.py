from typing import Any
from rest_framework import views
from jwt import InvalidTokenError

from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed

from django.core.mail import send_mail
from django.conf import settings

from portal.exceptions import PortalException
from portal.models.accounts import BlackListedAccessToken


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
    Insurance Coverage State: {requirements_request.insurance_coverage_state}\n
    CoverMyMeds Key: {requirements_request.member_details.cover_my_meds_key}\n
    App Release Version: {requirements_request.release_version}\n
    Submission Date: {requirements_request.submission_date}\n
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_TO_EMAIL], fail_silently=False)


def send_denial_notification(requirements_request):
    subject = "Denial Details Submitted"
    message = f"""
    DoPriorAuth user submitted denial details.\n\n
    Medication: {requirements_request.medication}\n
    CoverMyMeds Key: {requirements_request.member_details.cover_my_meds_key}\n
    App Release Version: {requirements_request.release_version}\n
    Submission Date: {requirements_request.submission_date}\n
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_TO_EMAIL], fail_silently=False)


class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        is_allowed_user = True
        try:
            access_token = request.auth.token.decode("utf-8")
        except InvalidTokenError:
            raise AuthenticationFailed('Activation token is invalid!')
        try:
            is_blacklisted = BlackListedAccessToken.objects.get(user=user_id, access_token=access_token)
            if is_blacklisted:
                is_allowed_user = False
        except BlackListedAccessToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user


class Is2FAVerified(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_2fa_verified)

mfa_enabled = settings.ENABLE_2FA
default_perms = (IsAuthenticated, IsTokenValid, Is2FAVerified) if mfa_enabled else (IsAuthenticated, IsTokenValid)


class SecuredAPIView(views.APIView):
    permission_classes = default_perms

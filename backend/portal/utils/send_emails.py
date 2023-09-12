from django.core.mail import EmailMessage
from django.conf import settings
from portal.utils.async_tasks import background_tasks_supported, try_run_in_background
from portal.tasks import send_notification_task
from enum import Enum


class ServiceEmail:
    def __init__(self, subject, message, from_email, to_email, bcc=[]):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.to_email = to_email
        self.bcc = bcc

    def send_email(self):
        email = EmailMessage(self.subject, self.message, self.from_email, self.to_email, self.bcc, fail_silently=False)
        email.send()


class ActivationEmail(ServiceEmail):
    def __init__(self, first_name, last_name, email, token, user_id_code):
        subject = f"Verify Your Account Now | {settings.ISSUER_NAME}"
        message = f"""
            Dear {first_name} {last_name},
            
            Welcome aboard! To continue, please click the link below to verify your account:
            {settings.WEBSITE_URL}confirm-email/{user_id_code}/{token}

            Best regards,
            The Do Prior Auth Team
        """
        super().__init__(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


class PasswordResetEmail(ServiceEmail):
    def __init__(self, reset_password_token):
        subject = f"Password Reset | {settings.ISSUER_NAME}"
        message = f"""
            Dear {reset_password_token.user.full_name()},

            Please click the following link to set up a new password. 
            {settings.WEBSITE_URL}password-reset/{reset_password_token.key}

            Best regards,
            The Do Prior Auth Team
        """
        super().__init__(subject, message, settings.DEFAULT_FROM_EMAIL, [reset_password_token.user.email])


class NotRegisteredPromoEmail(ServiceEmail):
    def __init__(self, email, first_name, last_name):
        subject = f"Set Up an Account | {settings.ISSUER_NAME}"
        message = f"""
            Dear {first_name} {last_name},

            Thank you for your interest! Someone from our team will be in contact with you. 

            Feel free to contact us anytime at founders@lamarhealth.com

            Best Regards,
            The Do Prior Auth Team
        """
        super().__init__(subject, message, settings.DEFAULT_FROM_EMAIL, [email], ["founders@lamarhealth.com"])


class RanOutOfSeatsEmail(ServiceEmail):
    def __init__(self, client_company, email, first_name, last_name):
        subject = f"{client_company} ran out of seats"
        message = f"""
            New user attempted to register at {settings.WEBSITE_URL} with {client_company} domain.
            {client_company.company_name} has ran out of seats.

            Contacts used:
            Name: {first_name} {last_name}
            Email: {email}

            Best regards,
            The Do Prior Auth Team
        """
        super().__init__(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


class DenialRequestEmail(ServiceEmail):
    def __init__(self, requirements_request):
        subject = "Denial Details Submitted"
        message = f"""
        DoPriorAuth user submitted denial details.\n\n
        Medication: {requirements_request.medication}\n
        CoverMyMeds Key: {requirements_request.member_details.cover_my_meds_key}\n
        App Release Version: {requirements_request.release_version}\n
        Submission Date: {requirements_request.submission_date}\n
        """
        super().__init__(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_TO_EMAIL])


class NewRequestEmail(ServiceEmail):
    def __init__(self, requirements_request):
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
        super().__init__(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_TO_EMAIL])


class NotificationType(Enum):
    NEW_REQUEST = NewRequestEmail
    DENIAL = DenialRequestEmail
    PASSWORD_RESET = PasswordResetEmail
    ACTIVATION = ActivationEmail
    NOT_REGISTERED_PROMO = NotRegisteredPromoEmail
    RAN_OUT_OF_SEATS = RanOutOfSeatsEmail


def send_notification(notification_type, *args):
    email = NotificationType[notification_type].value(*args)
    email.send_email()


def send_service_email(notification_type, *args, **kwargs):
    if not background_tasks_supported():
        send_notification(notification_type, *args, **kwargs)
    try_run_in_background(
        send_notification_task,
        args=[notification_type, args, kwargs],
        expires=120,
    )

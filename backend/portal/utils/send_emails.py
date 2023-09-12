from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from portal.utils.token import account_activation_token
from portal.models.auth import User


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


def send_password_reset_email(reset_password_token):
    subject = f"Password Reset | {settings.ISSUER_NAME}"
    message = f"""
        Dear {reset_password_token.user.full_name()},

        Please click the following link to set up a new password. 
        {settings.WEBSITE_URL}password-reset/{reset_password_token.key}

        Best regards,
        The Do Prior Auth Team
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [reset_password_token.user.email], fail_silently=False)


def send_activation_email(user_id):
    user = User.objects.get(pk=user_id)
    user_id_code = urlsafe_base64_encode(force_bytes(user_id))
    token = account_activation_token.make_token(user)
    subject = f"Verify Your Account Now | {settings.ISSUER_NAME}"
    message = f"""
        Dear {user.full_name()},
        
        Welcome aboard! To continue, please click the link below to verify your account:
        {settings.WEBSITE_URL}confirm-email/{user_id_code}/{token}

        Best regards,
        The Do Prior Auth Team
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)


def send_not_registered_promo_email(email, first_name, last_name):
    subject = f"Set Up an Account | {settings.ISSUER_NAME}"
    message = f"""
        Dear {first_name} {last_name},

        Thank you for your interest! Someone from our team will be in contact with you. 

        Feel free to contact us anytime at founders@lamarhealth.com

        Best Regards,
        The Do Prior Auth Team
    """
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        ["founders@lamarhealth.com"],
    )
    email.send()


def send_ran_out_of_seats(client_company, email, first_name, last_name):
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
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ["founders@lamarhealth.com"], fail_silently=False)

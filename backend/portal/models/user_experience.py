from django.db import models
from django.core.mail import send_mail
from django.conf import settings

from ._common import PortalModelBase


class UserExperience(PortalModelBase):
    is_helpful = models.BooleanField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)


class RequestUnavailableRequirements(PortalModelBase):
    medication = models.TextField(blank=True, null=True)
    insurance_provider = models.TextField(blank=True, null=True)
    insurance_plan_number = models.TextField(blank=True, null=True)
    insurance_coverage_state = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def send_notification(self):
        subject = "Request Unavailable Prior Auth Requirements"
        message = f"""
        DoPriorAuth user attempted a search but no prior auth requirements were found.\n\n
        Medication: {self.medication}\n
        Insurance Provider: {self.insurance_provider}\n
        Insurance Plan Number: {self.insurance_plan_number}\n
        Insurance Coverage State: {self.insurance_coverage_state}\n
        Comment: {self.comment}\n
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, settings.DEFAULT_TO_EMAIL, fail_silently=False)

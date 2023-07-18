from django.db import models

from ._common import PortalModelBase


class UXFeedback(PortalModelBase):
    is_helpful = models.BooleanField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    release_version = models.TextField(blank=True, null=True)


class RequestUnavailableRequirements(PortalModelBase):
    medication = models.TextField(blank=True, null=True)
    insurance_provider = models.TextField(blank=True, null=True)
    insurance_plan_number = models.TextField(blank=True, null=True)
    insurance_coverage_state = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    release_version = models.TextField(blank=True, null=True)

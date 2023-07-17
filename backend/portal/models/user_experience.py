from django.db import models
from ._common import PortalModelBase


class UserExperience(PortalModelBase):
    is_helpful = models.BooleanField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)


class RequestFeature(PortalModelBase):
    medication = models.TextField(blank=True, null=True)
    insurance_provider = models.TextField(blank=True, null=True)
    insurance_plan_number = models.TextField(blank=True, null=True)
    insurance_coverage_state = models.TextField(blank=True, null=True)

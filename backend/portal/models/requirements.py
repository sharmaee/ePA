from django.db import models

from ._common import PortalModelBase


class PriorAuthRequirement(PortalModelBase):
    insurance_provider = models.TextField(blank=True, null=True)
    insurance_plan_number = models.TextField(blank=True, null=True)
    insurance_coverage_state = models.TextField(blank=True, null=True)
    medication = models.TextField(blank=True, null=True)
    requirements_flow = models.TextField(blank=True, null=True)

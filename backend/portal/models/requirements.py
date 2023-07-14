from django.db import models
from ._common import PortalModelBase


class PriorAuthRequirement(PortalModelBase):
    insurance_provider = models.TextField(blank=True, null=True, db_index=True)
    insurance_plan_number = models.TextField(blank=True, null=True, db_index=True)
    insurance_coverage_state = models.TextField(blank=True, null=True, db_index=True)
    medication = models.TextField(blank=True, null=True, db_index=True)
    requirements_flow = models.TextField(blank=True, null=True)

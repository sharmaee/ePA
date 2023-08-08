from django.db import models

from ._common import PortalModelBase
from .requirements import PriorAuthRequirement


class UXFeedback(PortalModelBase):
    is_helpful = models.BooleanField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    release_version = models.TextField(blank=True, null=True)
    prior_auth_requirements = models.ForeignKey(PriorAuthRequirement, on_delete=models.CASCADE)

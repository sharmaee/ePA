from django.db import models

from ._common import PortalModelBase
from .requirements import PriorAuthRequirement
from .auth import User


class UXFeedback(PortalModelBase):
    is_helpful = models.BooleanField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    release_version = models.TextField(blank=True, null=True)
    prior_auth_requirements = models.ForeignKey(PriorAuthRequirement, on_delete=models.CASCADE, related_name="feedback")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ux_feedback")

    class Meta:
        verbose_name = 'UX Feedback'
        verbose_name_plural = 'UX Feedback'
        ordering = ['-created_on']

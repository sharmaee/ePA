from django.db import models
from portal.models._common import PortalModelBase
from portal.models.requirements import MemberDetails
from portal.models.auth import User


class PriorAuthDenial(PortalModelBase):
    medication = models.TextField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    release_version = models.TextField(blank=True, null=True)
    member_details = models.ForeignKey(MemberDetails, on_delete=models.CASCADE, related_name='denials')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='denials')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Denial'
        verbose_name_plural = 'Denials'
        ordering = ['-submission_date']

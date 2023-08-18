from django.db import models
from portal.models._common import PortalModelBase
from portal.models.requirements import MemberDetails


class PriorAuthDenial(PortalModelBase):
    medication = models.TextField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    release_version = models.TextField(blank=True, null=True)
    member_details = models.ForeignKey(MemberDetails, on_delete=models.CASCADE, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

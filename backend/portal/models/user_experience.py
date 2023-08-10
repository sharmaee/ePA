from django.db import models

from ._common import PortalModelBase, AES256EncryptedField
from .requirements import PriorAuthRequirement


class UXFeedback(PortalModelBase):
    is_helpful = models.BooleanField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    release_version = models.TextField(blank=True, null=True)
    requirements_date_modified = models.DateTimeField(blank=True, null=True)
    prior_auth_requirements = models.ForeignKey(PriorAuthRequirement, on_delete=models.CASCADE)
    email = AES256EncryptedField(blank=True, null=True)


class MemberDetails(PortalModelBase):
    email = AES256EncryptedField(blank=True, null=True)
    member_id = AES256EncryptedField(blank=True, null=True)
    first_name = AES256EncryptedField(blank=True, null=True)
    last_name = AES256EncryptedField(blank=True, null=True)
    dob = AES256EncryptedField(blank=True, null=True)
    zip_code = AES256EncryptedField(blank=True, null=True)


class RequestNewRequirements(PortalModelBase):
    medication = models.TextField(blank=True, null=True)
    insurance_provider = models.TextField(blank=True, null=True)
    insurance_plan_type = models.TextField(blank=True, null=True)
    insurance_coverage_state = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    release_version = models.TextField(blank=True, null=True)
    member_details = models.ForeignKey(MemberDetails, on_delete=models.CASCADE)

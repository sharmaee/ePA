from django.db import models
from ._common import PortalModelBase
from .field import AES256EncryptedField


class PriorAuthRequirement(PortalModelBase):
    url_slug = models.TextField(primary_key=True, db_index=True)
    description = models.TextField(blank=True, null=True, db_index=True)
    insurance_provider = models.TextField(blank=True, null=True, db_index=True)
    insurance_plan_type = models.TextField(blank=True, null=True, db_index=True)
    insurance_coverage_state = models.TextField(blank=True, null=True, db_index=True)
    medication = models.TextField(blank=True, null=True, db_index=True)
    requirements_checklist = models.JSONField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_modified = models.DateTimeField(auto_now=True, db_index=True)


class MemberDetails(PortalModelBase):
    first_name = AES256EncryptedField(blank=True, null=True)
    last_name = AES256EncryptedField(blank=True, null=True)
    dob = AES256EncryptedField(blank=True, null=True)
    email = AES256EncryptedField(blank=True, null=True)
    member_id = AES256EncryptedField(blank=True, null=True)
    phone_number = AES256EncryptedField(blank=True, null=True)
    address = AES256EncryptedField(blank=True, null=True)
    referring_doctor = AES256EncryptedField(blank=True, null=True)
    ma_email = AES256EncryptedField(blank=True, null=True)


class RequestNewPriorAuthRequirements(PortalModelBase):
    medication = models.TextField(blank=True, null=True)
    insurance_provider = models.TextField(blank=True, null=True)
    insurance_coverage_state = models.TextField(blank=True, null=True)
    insurance_plan_type = models.TextField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    release_version = models.TextField(blank=True, null=True)
    member_details = models.ForeignKey(MemberDetails, on_delete=models.CASCADE, blank=True, null=True)

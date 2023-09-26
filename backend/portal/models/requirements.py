from django.db import models
from portal.models._common import PortalModelBase
from portal.models.field import AES256EncryptedField
from portal.models.auth import User


class PriorAuthRequirement(PortalModelBase):
    url_slug = models.TextField(primary_key=True, db_index=True)
    description = models.TextField(blank=True, null=True, db_index=True)
    insurance_provider = models.TextField(blank=True, null=True, db_index=True)
    insurance_plan_type = models.TextField(blank=True, null=True, db_index=True)
    insurance_coverage_state = models.TextField(blank=True, null=True, db_index=True)
    medication = models.TextField(blank=True, null=True, db_index=True)
    requirements_checklist = models.JSONField(null=True)
    smart_engine_checklist = models.JSONField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_modified = models.DateTimeField(auto_now=True, db_index=True)


class MemberDetails(PortalModelBase):
    cover_my_meds_key = AES256EncryptedField(blank=True, null=True)
    last_name = AES256EncryptedField(blank=True, null=True)
    dob = AES256EncryptedField(blank=True, null=True)
    member_id = AES256EncryptedField(blank=True, null=True)

    def __str__(self):
        return f'{self.cover_my_meds_key} - {self.last_name} - {self.dob} - {self.member_id} - {self.ma_email}'


class RequestNewPriorAuthRequirements(PortalModelBase):
    medication = models.TextField(blank=True, null=True)
    insurance_provider = models.TextField(blank=True, null=True)
    insurance_coverage_state = models.TextField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    release_version = models.TextField(blank=True, null=True)
    member_details = models.ForeignKey(MemberDetails, on_delete=models.CASCADE, related_name='requests_new_pa')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_new_pa')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Request for More Info'
        verbose_name_plural = 'Requests for More Info'
        ordering = ['-submission_date']


class PriorAuthSubmission(PortalModelBase):
    cover_my_meds_key = models.TextField(primary_key=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requirements_alignment_completion')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

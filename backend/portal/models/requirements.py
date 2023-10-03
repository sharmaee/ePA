from django.db import models
from portal.models._common import PortalModelBase
from portal.models.field import AES256EncryptedField
from portal.models.auth import User


class Medication(PortalModelBase):
    medication_name = models.TextField(primary_key=True, db_index=True)
    description = models.TextField(blank=True, null=True, db_index=True)

    def __str__(self):
        return f'{self.medication_name}'


class PriorAuthRequirement(PortalModelBase):
    url_slug = models.TextField(primary_key=True, db_index=True)
    description = models.TextField(blank=True, null=True, db_index=True)
    insurance_provider = models.TextField(blank=True, null=True, db_index=True)
    insurance_plan_type = models.TextField(blank=True, null=True, db_index=True)
    insurance_coverage_state = models.TextField(blank=True, null=True, db_index=True)
    medication = models.ForeignKey(
        Medication, on_delete=models.CASCADE, related_name='prior_auth_requirements', blank=True, null=True
    )
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_modified = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return f'{self.insurance_provider} - {self.insurance_plan_type} - {self.insurance_coverage_state} - {self.medication}'


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


class NodeTypes(models.TextChoices):
    FIELDSET = 'fieldset'


class InputNodeTypes(models.TextChoices):
    RADIO = 'radio'
    CHECKBOX = 'checkbox'


class RequirementTemplate(PortalModelBase):
    requirement_rule_name = models.TextField(primary_key=True, db_index=True)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='requirement_templates')
    node_type = models.TextField(choices=NodeTypes.choices, default=NodeTypes.FIELDSET)
    label = models.TextField(blank=True, null=True)


class RequirementOptionTemplate(PortalModelBase):
    option_rule_name = models.TextField(primary_key=True, db_index=True)
    requirement_template = models.ForeignKey(
        RequirementTemplate, on_delete=models.CASCADE, related_name='requirement_option_templates'
    )
    node_type = models.TextField(choices=InputNodeTypes.choices, default=InputNodeTypes.RADIO)
    label = models.TextField(blank=True, null=True)


class SmartEngineItem(PortalModelBase):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='smart_engine_items')
    requirement_template = models.ForeignKey(
        RequirementTemplate, on_delete=models.CASCADE, related_name='smart_engine_items', blank=True, null=True
    )
    requirement_option_template = models.ForeignKey(
        RequirementOptionTemplate, on_delete=models.CASCADE, related_name='smart_engine_items', blank=True, null=True
    )
    label = models.TextField(blank=True, null=True)
    validation = models.TextField(blank=True, null=True)


class Requirement(PortalModelBase):
    prior_auth_requirement = models.ForeignKey(
        PriorAuthRequirement, on_delete=models.CASCADE, related_name='requirements'
    )
    requirement_template = models.ForeignKey(RequirementTemplate, on_delete=models.CASCADE, related_name='requirements')
    smart_engine_items = models.ManyToManyField(SmartEngineItem, related_name='requirements')
    requirement_rule_set = models.JSONField(blank=True, null=True)


class RequirementOption(PortalModelBase):
    prior_auth_requirement = models.ForeignKey(
        PriorAuthRequirement, on_delete=models.CASCADE, related_name='requirement_options'
    )
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name='requirement_options')
    requirement_option_template = models.ForeignKey(
        RequirementOptionTemplate, on_delete=models.CASCADE, related_name='requirement_options'
    )
    smart_engine_items = models.ManyToManyField(SmartEngineItem, related_name='requirement_options')
    option_rule_set = models.JSONField(blank=True, null=True)

from django.db import models
from portal.models._common import PortalModelBase, slugify
from portal.models.field import AES256EncryptedField
from portal.models.auth import User


class Medication(PortalModelBase):
    medication = models.TextField(primary_key=True, db_index=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.medication}'


class State(PortalModelBase):
    state = models.TextField(primary_key=True, db_index=True)

    def __str__(self):
        return f'{self.state}'


class InsurancePlanType(PortalModelBase):
    insurance_plan_type = models.TextField(primary_key=True, db_index=True)

    def __str__(self):
        return f'{self.insurance_plan_type}'


class InsuranceProvider(PortalModelBase):
    insurance_provider = models.TextField(primary_key=True, db_index=True)

    def __str__(self):
        return f'{self.insurance_provider}'


class PriorAuthRequirement(PortalModelBase):
    url_slug = models.TextField(primary_key=True, db_index=True)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='prior_auth_requirements')
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE, related_name='prior_auth_requirements')
    insurance_plan_types = models.ManyToManyField(InsurancePlanType, related_name='prior_auth_requirements')
    insurance_coverage_states = models.ManyToManyField(State, related_name='prior_auth_requirements')

    def __str__(self):
        return f'{self.insurance_provider} - {self.medication}'
    
    def save(self, *args, **kwargs):
        if not self.url_slug:
            self.url_slug = slugify()
        super().save(*args, **kwargs)


class MemberDetails(PortalModelBase):
    cover_my_meds_key = AES256EncryptedField(blank=True, null=True)
    last_name = AES256EncryptedField(blank=True, null=True)
    dob = AES256EncryptedField(blank=True, null=True)
    member_id = AES256EncryptedField(blank=True, null=True)

    def __str__(self):
        return f'{self.cover_my_meds_key} - {self.last_name} - {self.dob} - {self.member_id}'


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
    requirement_template = models.TextField(primary_key=True, db_index=True)    # xxhash medication + _ + requirement_rule_name
    requirement_rule_name = models.TextField(editable=False)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='requirement_templates')
    node_type = models.TextField(choices=NodeTypes.choices, default=NodeTypes.FIELDSET)
    label = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.label}'    


class RequirementOptionTemplate(PortalModelBase):
    requirement_option_template = models.TextField(primary_key=True, db_index=True)    # xxhash medication + _ + option_rule_name
    option_rule_name = models.TextField(editable=False)
    requirement_template = models.ForeignKey(
        RequirementTemplate, on_delete=models.CASCADE, related_name='requirement_option_templates'
    )
    node_type = models.TextField(choices=InputNodeTypes.choices, default=InputNodeTypes.RADIO)
    label = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.label}'


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

    def __str__(self):
        return f'{self.label}'


class Requirement(PortalModelBase):
    prior_auth_requirement = models.ForeignKey(
        PriorAuthRequirement, on_delete=models.CASCADE, related_name='requirements'
    )
    requirement_template = models.ForeignKey(RequirementTemplate, on_delete=models.CASCADE, related_name='requirements')
    smart_engine_items = models.ManyToManyField(SmartEngineItem, related_name='requirements')
    requirement_rule_set = models.JSONField(blank=True, null=True)


class RequirementOption(PortalModelBase):
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name='requirement_options')
    requirement_option_template = models.ForeignKey(
        RequirementOptionTemplate, on_delete=models.CASCADE, related_name='requirement_options'
    )
    smart_engine_items = models.ManyToManyField(SmartEngineItem, related_name='requirement_options')
    option_rule_set = models.JSONField(blank=True, null=True)

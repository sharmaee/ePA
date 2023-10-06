from django.db import models
from portal.models._common import PortalModelBase, slugify
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


class InsuranceCoverageCriteria(PortalModelBase):
    url_slug = models.TextField(primary_key=True, db_index=True)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='insurance_coverage_criteria')
    insurance_provider = models.ForeignKey(
        InsuranceProvider, on_delete=models.CASCADE, related_name='insurance_coverage_criteria'
    )
    insurance_plan_types = models.ManyToManyField(
        InsurancePlanType,
        related_name='insurance_coverage_criteria',
        db_table='requirements__insuranceplantype_to_insurancecoveragecriteria',
        blank=True,
    )
    states = models.ManyToManyField(
        State,
        related_name='insurance_coverage_criteria',
        db_table='requirements__state_to_insurancecoveragecriteria',
        blank=True,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.insurance_provider} - {self.medication}'

    def save(self, *args, **kwargs):
        if not self.url_slug:
            self.url_slug = slugify()
        super().save(*args, **kwargs)


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

    def __str__(self):
        return f'{self.label}'


class RequirementOptionTemplate(PortalModelBase):
    option_rule_name = models.TextField(primary_key=True, db_index=True)
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
    insurance_coverage_criteria = models.ForeignKey(
        InsuranceCoverageCriteria, on_delete=models.CASCADE, related_name='requirements'
    )
    requirement_template = models.ForeignKey(RequirementTemplate, on_delete=models.CASCADE, related_name='requirements')
    smart_engine_items = models.ManyToManyField(
        SmartEngineItem, related_name='+', db_table='requirements__smartengineitem_to_requirement', blank=True
    )
    requirement_rule_set = models.ManyToManyField(
        RequirementTemplate, related_name='+', db_table='requirements__requirementtemplate_to_requirement', blank=True
    )

    def __str__(self):
        return f'{self.requirement_template} | {self.insurance_coverage_criteria}'


class RequirementOption(PortalModelBase):
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name='requirement_options')
    requirement_option_template = models.ForeignKey(
        RequirementOptionTemplate, on_delete=models.CASCADE, related_name='requirement_options'
    )
    smart_engine_items = models.ManyToManyField(
        SmartEngineItem, related_name='+', db_table='requirements__smartengineitem_to_requirement_option', blank=True
    )
    option_rule_set = models.ManyToManyField(
        RequirementOptionTemplate,
        related_name='+',
        db_table='requirements__requirementoptiontemplate_to_requirement',
        blank=True,
    )

    def __str__(self):
        return f'{self.requirement_option_template} | {self.requirement.insurance_coverage_criteria}'

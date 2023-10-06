from django.contrib import admin
from portal.models.requirements import (
    Medication,
    State,
    InsurancePlanType,
    InsuranceProvider,
    InsuranceCoverageCriteria,
    RequirementTemplate,
    RequirementOptionTemplate,
    SmartEngineItem,
    Requirement,
    RequirementOption,
)


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('medication',)
    search_fields = ('medication',)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('state',)
    search_fields = ('state',)


@admin.register(InsurancePlanType)
class InsurancePlanTypeAdmin(admin.ModelAdmin):
    list_display = ('insurance_plan_type',)
    search_fields = ('insurance_plan_type',)


@admin.register(InsuranceProvider)
class InsuranceProviderAdmin(admin.ModelAdmin):
    list_display = ('insurance_provider',)
    search_fields = ('insurance_provider',)


@admin.register(InsuranceCoverageCriteria)
class InsuranceCoverageCriteriaAdmin(admin.ModelAdmin):
    list_display = (
        'medication',
        'insurance_provider',
        'created_on',
    )
    search_fields = (
        'medication',
        'insurance_provider',
    )


@admin.register(RequirementTemplate)
class RequirementTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'requirement_rule_name',
        'medication',
        'label',
    )
    search_fields = (
        'requirement_rule_name',
        'medication',
    )


@admin.register(RequirementOptionTemplate)
class RequirementOptionTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'option_rule_name',
        'requirement_template',
        'label',
    )
    search_fields = (
        'option_rule_name',
        'requirement_template',
    )


@admin.register(SmartEngineItem)
class SmartEngineItemAdmin(admin.ModelAdmin):
    list_display = (
        'label',
        'validation',
    )
    search_fields = (
        'label',
        'validation',
    )


@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = (
        'insurance_coverage_criteria',
        'requirement_template',
    )
    search_fields = (
        'insurance_coverage_criteria',
        'requirement_template',
    )


@admin.register(RequirementOption)
class RequirementOptionAdmin(admin.ModelAdmin):
    list_display = (
        'requirement',
        'requirement_option_template',
    )
    search_fields = (
        'requirement',
        'requirement_option_template',
    )

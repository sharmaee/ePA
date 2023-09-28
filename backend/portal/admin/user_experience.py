from django.contrib import admin

from portal.models.user_experience import UXFeedback
from portal.models.auth import User
from portal.models.requirements import PriorAuthRequirement
from import_export.admin import ExportActionModelAdmin
from rangefilter.filter import DateRangeFilter
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget


class UXFeedbackResource(resources.ModelResource):
    user = fields.Field(
        column_name='user', attribute='user', widget=ForeignKeyWidget(User, field='email')
    )
    prior_auth_requirements = fields.Field(
        column_name='prior_auth_requirements',
        attribute='prior_auth_requirements', 
        widget=ForeignKeyWidget(PriorAuthRequirement, field='insurance_provider')
    )
    class Meta:
        model = UXFeedback
        fields = ('is_helpful', 'comment', 'created_on', 'release_version', 'prior_auth_requirements', 'user')


class RequirementsSearchActionAdmin(ExportActionModelAdmin):
    list_display = (
        'is_helpful',
        'comment',
        'insurance_provider',
        'insurance_coverage_state',
        'insurance_plan_type',
        'created_by_user',
        'medication',
        'release_version',
        'created_on',
    )
    list_filter = (
        ('created_on', DateRangeFilter),
        'created_on',
        'user',
        'prior_auth_requirements',
        'is_helpful',
        'release_version',
    )
    search_fields = (
        'prior_auth_requirements__insurance_provider',
        'prior_auth_requirements__insurance_coverage_state',
        'prior_auth_requirements__insurance_plan_type',
        'prior_auth_requirements__medication',
        'is_helpful',
        'comment',
        'user__email',
    )
    resource_class = UXFeedbackResource

    def created_by_user(self, obj):
        return obj.user.email

    def insurance_provider(self, obj):
        return obj.prior_auth_requirements.insurance_provider
    
    def insurance_coverage_state(self, obj):
        return obj.prior_auth_requirements.insurance_coverage_state
    
    def insurance_plan_type(self, obj):
        return obj.prior_auth_requirements.insurance_plan_type
    
    def medication(self, obj):
        return obj.prior_auth_requirements.medication

admin.site.register(UXFeedback, RequirementsSearchActionAdmin)

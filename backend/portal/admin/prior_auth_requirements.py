from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ExportActionModelAdmin

from portal.models.requirements import RequestNewPriorAuthRequirements, PriorAuthSubmission
from portal.models.pa_denial import PriorAuthDenial
from portal.models.auth import User


base_display_member_details_fields = (
    'cover_my_meds_key',
    'last_name',
    'dob',
    'member_id',
    'ma_email',
)

base_display_fields = (
    'submission_date',
    'notes',
)


class AnalyticsAdminBase(admin.ModelAdmin):
    list_per_page = 100

    def has_add_permission(self, *_):
        return False

    def has_delete_permission(self, *_):
        return False


class DisplayMemberDetailsAdmin(AnalyticsAdminBase):
    def cover_my_meds_key(self, obj):
        return obj.member_details.cover_my_meds_key

    def last_name(self, obj):
        return obj.member_details.last_name

    def dob(self, obj):
        return obj.member_details.dob

    def member_id(self, obj):
        return obj.member_details.member_id

    def ma_email(self, obj):
        return obj.user.email


@admin.register(RequestNewPriorAuthRequirements)
class RequestNewPriorAuthRequirementsAdmin(DisplayMemberDetailsAdmin):
    list_display = (
        base_display_fields
        + base_display_member_details_fields
        + (
            'insurance_provider',
            'insurance_coverage_state',
        )
    )
    list_filter = (
        'insurance_provider',
        'insurance_coverage_state',
        'submission_date',
    )
    search_fields = (
        'insurance_provider',
        'insurance_coverage_state',
        'member_details__last_name',
    )


@admin.register(PriorAuthDenial)
class PriorAuthDenialAdmin(DisplayMemberDetailsAdmin):
    list_display = base_display_fields + base_display_member_details_fields

    list_filter = ('submission_date',)


class PriorAuthSubmissionResource(resources.ModelResource):
    user = fields.Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, field='email'))

    class Meta:
        model = PriorAuthSubmission
        fields = ('created_on', 'updated_on', 'user', 'cover_my_meds_key')


class PriorAuthSubmissionAdmin(ExportActionModelAdmin):
    list_display = (
        'cover_my_meds_key',
        'created_by_user',
        'created_on',
        'updated_on',
    )
    list_filter = (
        ('created_on', DateRangeFilter),
        ('updated_on', DateRangeFilter),
        'user',
        'created_on',
        'updated_on',
    )
    search_fields = (
        'cover_my_meds_key',
        'user__email',
    )
    resource_class = PriorAuthSubmissionResource

    def created_by_user(self, obj):
        return obj.user.email


admin.site.register(PriorAuthSubmission, PriorAuthSubmissionAdmin)

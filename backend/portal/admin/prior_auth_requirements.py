from django.contrib import admin

from portal.models.requirements import RequestNewPriorAuthRequirements
from portal.models.pa_denial import PriorAuthDenial


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

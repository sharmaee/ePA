from django.contrib import admin

from portal.models.analytics import RequirementsSearchAction
from portal.models.auth import User
from import_export.admin import ExportActionModelAdmin
from rangefilter.filter import DateRangeFilter
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget


class RequirementsSearchActionResource(resources.ModelResource):
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(User, field='email'))

    class Meta:
        model = RequirementsSearchAction
        fields = (
            'insurance_provider',
            'insurance_coverage_state',
            'medication',
            'created_on',
            'created_by'
        )


class RequirementsSearchActionAdmin(ExportActionModelAdmin):
    list_display = (
        'insurance_provider',
        'insurance_coverage_state',
        'medication',
        'created_on',
        'created_by_user',
    )
    list_filter = (('created_on', DateRangeFilter), 'created_on', 'created_by', 'insurance_coverage_state', 'insurance_provider', 'medication')
    search_fields = (
        'insurance_provider',
        'insurance_coverage_state',
        'medication',
        'created_by__email',
    )
    resource_class = RequirementsSearchActionResource

    def created_by_user(self, obj):
        return obj.created_by.email


admin.site.register(RequirementsSearchAction, RequirementsSearchActionAdmin)

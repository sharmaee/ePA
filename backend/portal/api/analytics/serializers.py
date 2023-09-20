from rest_framework import serializers
from portal.models.analytics import RequirementsSearchAction


class ActionMetaBase:
    exclude = ['created_by']


class RequirementsSearchActionSerializer(serializers.ModelSerializer):
    class Meta(ActionMetaBase):
        model = RequirementsSearchAction

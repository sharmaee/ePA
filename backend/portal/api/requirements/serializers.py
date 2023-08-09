from dotmap import DotMap
from rest_framework import serializers

from portal.models.requirements import (
    PriorAuthRequirement,
)
from portal.api.common import ObjSerializer, UnvalidatedField


class PriorAuthRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorAuthRequirement
        fields = (
            'url_slug',
            'description',
            'insurance_provider',
            'insurance_plan_number',
            'insurance_plan_type',
            'insurance_coverage_state',
            'medication',
        )
        read_only_fields = fields


class PriorAuthRequirementDetailSerializer(PriorAuthRequirementSerializer):
    class Meta:
        model = PriorAuthRequirement
        fields = PriorAuthRequirementSerializer.Meta.fields + (
            'requirements_flow',
            'requirements_flow_file_location',
            'requirements_checklist',
        )


class AvailableSearchOptionsSerializer(ObjSerializer):
    insurance_providers = serializers.ListField(child=serializers.CharField())
    insurance_plan_types = serializers.ListField(child=serializers.CharField())
    insurance_plan_numbers = serializers.ListField(child=serializers.CharField())
    insurance_coverage_states = serializers.ListField(child=serializers.CharField())
    medications = serializers.ListField(child=serializers.CharField())
    insurance_plans_by_provider = serializers.DictField(child=serializers.ListField(child=serializers.CharField()))

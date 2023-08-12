from rest_framework import serializers

from portal.models.requirements import (
    PriorAuthRequirement,
    RequestNewPriorAuthRequirements,
    MemberDetails,
)
from portal.api.common import ObjSerializer


class PriorAuthRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorAuthRequirement
        fields = (
            'url_slug',
            'description',
            'insurance_provider',
            'insurance_plan_type',
            'insurance_coverage_state',
            'medication',
        )
        read_only_fields = fields


class PriorAuthRequirementDetailSerializer(PriorAuthRequirementSerializer):
    class Meta:
        model = PriorAuthRequirement
        fields = PriorAuthRequirementSerializer.Meta.fields + ('requirements_checklist',)


class AvailableSearchOptionsSerializer(ObjSerializer):
    insurance_providers = serializers.ListField(child=serializers.CharField())


class MemberDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberDetails
        fields = '__all__'


class RequestNewPriorAuthRequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestNewPriorAuthRequirements
        fields = '__all__'

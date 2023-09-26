from rest_framework import serializers

from portal.models.requirements import (
    PriorAuthRequirement,
    RequestNewPriorAuthRequirements,
    MemberDetails,
    PriorAuthSubmission,
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
        fields = PriorAuthRequirementSerializer.Meta.fields + ('requirements_checklist', 'smart_engine_checklist')


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


class PriorAuthSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorAuthSubmission
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get("request", None)
        user = request.user if request and hasattr(request, "user") else None
        obj, created = PriorAuthSubmission.objects.update_or_create(
            cover_my_meds_key=validated_data.get("cover_my_meds_key", None), user=user
        )
        return obj

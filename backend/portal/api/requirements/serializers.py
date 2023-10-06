from rest_framework import serializers
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from portal.models.requirements import (
    PriorAuthRequirement,
    RequestNewPriorAuthRequirements,
    MemberDetails,
    PriorAuthSubmission,
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


class AvailableSearchOptionsSerializer(ObjSerializer):
    insurance_providers = serializers.ListField(child=serializers.CharField())
    medications = serializers.ListField(child=serializers.CharField())


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


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ('medication',)


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class InsurancePlanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePlanType
        fields = '__all__'


class InsuranceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceProvider
        fields = '__all__'


class InsuranceCoverageCriteriaSerializer(serializers.ModelSerializer):
    url_slug = serializers.SerializerMethodField()

    class Meta:
        model = InsuranceCoverageCriteria
        fields = (
            'url_slug',
            'medication',
            'insurance_provider',
            'states',
            'insurance_plan_types',
        )

    def get_url_slug(self, obj):
        return urlsafe_base64_encode(force_bytes(obj.url_slug))


class SmartEngineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartEngineItem
        fields = (
            'label',
            'validation',
        )


class RequirementTemplateSerializer(serializers.ModelSerializer):
    smart_engine_items = SmartEngineItemSerializer(many=True)

    class Meta:
        model = RequirementTemplate
        fields = (
            'requirement_rule_name',
            'node_type',
            'label',
            'smart_engine_items',
        )


class RequirementOptionTemplateSerializer(serializers.ModelSerializer):
    smart_engine_items = SmartEngineItemSerializer(many=True)

    class Meta:
        model = RequirementOptionTemplate
        fields = (
            'option_rule_name',
            'node_type',
            'label',
            'smart_engine_items',
        )


class RequirementOptionRuleSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequirementOptionTemplate
        fields = ('option_rule_name',)


class RequirementOptionSerializer(serializers.ModelSerializer):
    requirement_option_template = RequirementOptionTemplateSerializer()

    class Meta:
        model = RequirementOption
        fields = (
            'requirement_option_template',
            'option_rule_set',
        )


class RequirementRuleSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequirementTemplate
        fields = ('requirement_rule_name',)


class RequirementSerializer(serializers.ModelSerializer):
    requirement_template = RequirementTemplateSerializer()
    requirement_options = RequirementOptionSerializer(many=True)

    class Meta:
        model = Requirement
        fields = (
            'requirement_template',
            'requirement_rule_set',
            'requirement_options',
        )

from rest_framework import serializers

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
        fields = '__all__'


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
    medication = MedicationSerializer()
    insurance_provider = InsuranceProviderSerializer()
    states = StateSerializer(many=True)
    insurance_plan_types = InsurancePlanTypeSerializer(many=True)

    class Meta:
        model = InsuranceCoverageCriteria
        fields = '__all__'


class RequirementTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequirementTemplate
        fields = '__all__'


class RequirementOptionTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequirementOptionTemplate
        fields = '__all__'


class SmartEngineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartEngineItem
        fields = (
            'label',
            'validation',
        )


class RequirementOptionSerializer(serializers.ModelSerializer):
    requirement_option_template = RequirementOptionTemplateSerializer()
    smart_engine_items = SmartEngineItemSerializer(many=True)

    class Meta:
        model = RequirementOption
        fields = (
            'requirement_option_template',
            'smart_engine_items',
            'option_rule_set',
        )


class RequirementSerializer(serializers.ModelSerializer):
    requirement_template = RequirementTemplateSerializer()
    smart_engine_items = SmartEngineItemSerializer(many=True)
    options = serializers.SerializerMethodField()

    class Meta:
        model = Requirement
        fields = (
            'requirement_template',
            'smart_engine_items',
            'requirement_rule_set',
            'options',
        )

    def get_options(self, obj):
        options = RequirementOption.objects.filter(requirement=obj).select_related('requirement_option_template')
        return RequirementOptionSerializer(options, many=True).data

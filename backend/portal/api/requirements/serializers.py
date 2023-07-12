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
            'insurance_provider', 'insurance_plan_number', 'insurance_coverage_state', 'medication', 'requirements_flow'
        )
        read_only_fields = fields

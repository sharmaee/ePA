from rest_framework import serializers
from portal.models.pa_denial import PriorAuthDenial


class PriorAuthDenialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorAuthDenial
        fields = '__all__'

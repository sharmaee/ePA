from rest_framework import serializers
from portal.models.pa_denial import PriorAuthDenial


class SubmitDenialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorAuthDenial
        fields = ('medication', 'cover_my_meds_key', 'ma_email')
        read_only_fields = fields

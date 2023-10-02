from rest_framework import serializers
from portal.models.user_experience import UXFeedback


class UXFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UXFeedback
        fields = '__all__'

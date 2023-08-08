from rest_framework import serializers

from portal.models.user_experience import UXFeedback


class UXFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UXFeedback
        fields = ('is_helpful', 'comment', 'release_version', 'submission_date')
        read_only_fields = fields

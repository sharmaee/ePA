from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from portal.models.user_experience import UXFeedback
from portal.models.requirements import PriorAuthRequirement


class UXFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UXFeedback
        fields = '__all__'

    def create(self, validated_data):
        is_helpful = validated_data['is_helpful']
        email = validated_data.get('email', '')

        feedback = UXFeedback.objects.create(
            is_helpful=is_helpful,
            comment=validated_data.get('comment', ''),
            release_version=validated_data.get('release_version', ''),
            prior_auth_requirements=validated_data.get('prior_auth_requirements', ''),
            email=email,
        )
        feedback.save()

        if email and is_helpful == False:
            subject = "User Experience Feedback"
            message = f"""
            DoPriorAuth user submitted feedback.\n\n
            How can we improve: {feedback.comment}\n\n
            App Release Version: {feedback.release_version}\n
            Submission Date: {feedback.submission_date}\n
            Insurance Provider: {feedback.prior_auth_requirements.insurance_provider}\n
            Plan Type: {feedback.prior_auth_requirements.insurance_plan_type}\n
            Coverage State: {feedback.prior_auth_requirements.insurance_coverage_state}\n
            """
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_TO_EMAIL], fail_silently=False)

        return feedback


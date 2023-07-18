from rest_framework import serializers

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from portal.models.user_experience import UXFeedback, RequestUnavailableRequirements


class UXFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UXFeedback
        fields = ('is_helpful', 'comment', 'release_version', 'submission_date')
        read_only_fields = fields


class RequestUnavailableRequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestUnavailableRequirements
        fields = (
            'medication',
            'insurance_provider',
            'insurance_plan_number',
            'insurance_coverage_state',
            'comment',
            'release_version',
            'submission_date',
        )
        read_only_fields = fields

    def create(self, validated_data):
        requirements_request = RequestUnavailableRequirements.objects.create(
            medication=validated_data.get('medication', ''),
            insurance_provider=validated_data.get('insurance_provider', ''),
            insurance_plan_number=validated_data.get('insurance_plan_number', ''),
            insurance_coverage_state=validated_data.get('insurance_coverage_state', ''),
            submission_date=timezone.now(),
        )

        requirements_request.save()
        subject = "Request for Unavailable Prior Auth Requirements"
        message = f"""
        DoPriorAuth user attempted a search but no prior auth requirements were found.\n\n
        Medication: {self.medication}\n
        Insurance Provider: {self.insurance_provider}\n
        Insurance Plan Number: {self.insurance_plan_number}\n
        Insurance Coverage State: {self.insurance_coverage_state}\n
        Comment: {self.comment}\n\n
        App Release Version: {self.release_version}\n
        Submission Date: {self.submission_date}\n
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, settings.DEFAULT_TO_EMAIL, fail_silently=False)

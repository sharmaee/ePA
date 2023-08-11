from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from portal.models.user_experience import UXFeedback
from portal.models.requirements import PriorAuthRequirement


class UXFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UXFeedback
        fields = ('is_helpful', 'comment', 'release_version', 'submission_date', 'requirements_date_modified')
        read_only_fields = fields
    
    def create(self, validated_data):
        is_helpful = validated_data.get('is_helpful', '')
        email = validated_data.get('email', '')

        feedback = UXFeedback.objects.create(
            is_helpful=validated_data.get('is_helpful'),
            comment=validated_data.get('comment', ''),
            submission_date=timezone.now(),
            release_version=validated_data.get('release_version', ''),
            requirements_date_modified=validated_data.get('requirements_date_modified', ''),
            prior_auth_requirements_id=validated_data.get('prior_auth_requirements', ''),
            email=validated_data.get('email', '')
        )
        feedback.save()

        if email and is_helpful == False:
            requirements = PriorAuthRequirement.objects.filter(url_slug = feedback.prior_auth_requirements).first()
            
            subject = "User Experience Feedback"
            message = f"""
            DoPriorAuth user submitted feedback.\n\n
            How can we improve: {self.comment}\n\n
            App Release Version: {self.release_version}\n
            Submission Date: {self.submission_date}\n
            Requirements Date Modified: {self.requirements_date_modified}\n
            Prior Auth Details: {requirements.insurance_provider} | 
            {requirements.insurance_plan_type}, {requirements.insurance_coverage_state}\n
            """
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, settings.DEFAULT_TO_EMAIL, fail_silently=False)

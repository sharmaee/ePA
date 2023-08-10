from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from portal.models.user_experience import UXFeedback, RequestNewRequirements, MemberDetails
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


class RequestNewRequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestNewRequirements
        fields = (
            'medication',
            'insurance_provider',
            'insurance_plan_type',
            'insurance_coverage_state',
            'comment',
            'release_version',
            'submission_date',
        )
        read_only_fields = fields

    def create(self, validated_data):
        requirements_request = RequestNewRequirements.objects.create(
            medication=validated_data.get('medication', ''),
            insurance_provider=validated_data.get('insurance_provider', ''),
            insurance_plan_number=validated_data.get('insurance_plan_number', ''),
            insurance_coverage_state=validated_data.get('insurance_coverage_state', ''),
            submission_date=timezone.now(),
        )
        requirements_request.save()

        member_details = MemberDetails.objects.create(
            email=validated_data.get('email', ''),
            member_id=validated_data.get('member_id', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            dob=validated_data.get('dob', ''),
            zip_code=validated_data.get('zip_code', ''),
        )
        member_details.save()

        subject = "Request for New Prior Auth Requirements"
        message = f"""
        DoPriorAuth user requested new prior auth requirements.\n\n
        Medication: {self.medication}\n
        Insurance Provider: {self.insurance_provider}\n
        Insurance Plan Type: {self.insurance_plan_type}\n
        Insurance Coverage State: {self.insurance_coverage_state}\n
        Comment: {self.comment}\n\n
        App Release Version: {self.release_version}\n
        Submission Date: {self.submission_date}\n
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, settings.DEFAULT_TO_EMAIL, fail_silently=False)

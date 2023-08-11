from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from portal.models.requirements import (
    PriorAuthRequirement,
    RequestNewPriorAuthRequirements,
    MemberDetails,
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


class PriorAuthRequirementDetailSerializer(PriorAuthRequirementSerializer):
    class Meta:
        model = PriorAuthRequirement
        fields = PriorAuthRequirementSerializer.Meta.fields + (
            'requirements_flow',  # TODO delete once confirmed not needed
            'requirements_flow_file_location',  # TODO delete once confirmed not needed
            'requirements_checklist',
        )


class AvailableSearchOptionsSerializer(ObjSerializer):
    insurance_providers = serializers.ListField(child=serializers.CharField())


class RequestNewPriorAuthRequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestNewPriorAuthRequirements
        fields = (
            'medication',
            'insurance_provider',
            'insurance_coverage_state',
            'release_version',
            'submission_date',
        )
        read_only_fields = fields

    def create(self, validated_data):
        member_details = MemberDetails.objects.create(
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            dob=validated_data.get('dob', ''),
            email=validated_data.get('email', ''),
            member_id=validated_data.get('member_id', ''),
            address=validated_data.get('address', ''),
            referring_doctor=validated_data.get('referring_doctor', ''),
            ma_email=validated_data.get('ma_email', ''),
        )
        member_details.save()

        requirements_request = RequestNewPriorAuthRequirements.objects.create(
            medication=validated_data.get('medication', ''),
            insurance_provider=validated_data.get('insurance_provider', ''),
            insurance_coverage_state=validated_data.get('insurance_coverage_state', ''),
            submission_date=timezone.now(),
            release_version=validated_data.get('release_version', ''),
            member_details=member_details,
        )
        requirements_request.save()

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

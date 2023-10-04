from rest_framework import status
from rest_framework.response import Response
from portal.utils.send_emails import send_service_email, NotificationType

from .serializers import (
    AvailableSearchOptionsSerializer,
    RequestNewPriorAuthRequirementsSerializer,
    MemberDetailsSerializer,
    PriorAuthSubmissionSerializer,
    InsuranceCoverageCriteriaSerializer,
)
from portal.api.utils import SecuredAPIView
from portal.logic.search.search_requirements import run_search, get_available_search_options
from portal.models.requirements import PriorAuthRequirement, PriorAuthSubmission


class PriorAuthRequirementsView(SecuredAPIView):
    def get(self, request):
        available_search_options = get_available_search_options()
        result = AvailableSearchOptionsSerializer(available_search_options).data
        return Response(result, status=status.HTTP_200_OK)


class PriorAuthRequirementSearchView(SecuredAPIView):
    def post(self, request):
        requirements = run_search(self.request.data)
        result = InsuranceCoverageCriteriaSerializer(requirements, many=True).data
        return Response(result, status=status.HTTP_200_OK)


class RequestNewPriorAuthRequirementsView(SecuredAPIView):
    def post(self, request):
        member_details = MemberDetailsSerializer(data=self.request.data)
        if member_details.is_valid(raise_exception=True):
            member_details.save()
            request_new_prior_auth_requirements = RequestNewPriorAuthRequirementsSerializer(
                data=request.data, partial=True
            )
            if request_new_prior_auth_requirements.is_valid(raise_exception=True):
                request_new_prior_auth_requirements.save(member_details=member_details.instance, user=self.request.user)
                new_request = request_new_prior_auth_requirements.instance
                send_service_email(
                    NotificationType.NEW_REQUEST,
                    new_request.medication,
                    new_request.member_details.cover_my_meds_key,
                    new_request.release_version,
                    new_request.submission_date,
                    self.request.user.email,
                )
                return Response(request_new_prior_auth_requirements.data, status=status.HTTP_200_OK)
        return Response(request_new_prior_auth_requirements.errors, status=status.HTTP_400_BAD_REQUEST)


class PriorAuthSubmissionView(SecuredAPIView):
    def post(self, request):
        cover_my_meds_key = self.request.data.get("cover_my_meds_key", None)
        if cover_my_meds_key is None:
            return Response({"cover_my_meds_key": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        obj, created = PriorAuthSubmission.objects.update_or_create(
            cover_my_meds_key=cover_my_meds_key, user=self.request.user
        )
        return Response(PriorAuthSubmissionSerializer(obj).data, status=status.HTTP_200_OK)

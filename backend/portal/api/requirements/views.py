from rest_framework import status
from rest_framework.response import Response
from portal.utils.send_emails import send_service_email, NotificationType

from .serializers import (
    PriorAuthRequirementSerializer,
    AvailableSearchOptionsSerializer,
    PriorAuthRequirementDetailSerializer,
    RequestNewPriorAuthRequirementsSerializer,
    MemberDetailsSerializer,
)
from portal.api.utils import SecuredAPIView
from portal.logic.search.search_requirements import run_search, get_available_search_options
from portal.models import PriorAuthRequirement


class PriorAuthRequirementsView(SecuredAPIView):
    def get(self, request):
        available_providers = get_available_search_options()
        result = AvailableSearchOptionsSerializer(available_providers).data
        return Response(result, status=status.HTTP_200_OK)


class PriorAuthRequirementSearchView(SecuredAPIView):
    def post(self, request):
        requirements = run_search(self.request.data)
        result = PriorAuthRequirementSerializer(requirements, many=True).data
        return Response(result, status=status.HTTP_200_OK)


class PriorAuthRequirementDetailView(SecuredAPIView):
    def get(self, request, url_slug):
        try:
            requirement = PriorAuthRequirementDetailSerializer(PriorAuthRequirement.objects.get(url_slug=url_slug)).data
        except PriorAuthRequirement.DoesNotExist:
            requirement = None
        return Response(requirement, status=status.HTTP_200_OK)


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
                send_service_email(
                    NotificationType.NEW_REQUEST.name,
                    request_new_prior_auth_requirements.instance.medication,
                    request_new_prior_auth_requirements.instance.insurance_provider,
                    request_new_prior_auth_requirements.instance.insurance_coverage_state,
                    request_new_prior_auth_requirements.instance.member_details.cover_my_meds_key,
                    request_new_prior_auth_requirements.instance.release_version,
                    request_new_prior_auth_requirements.instance.submission_date,
                )
                return Response(request_new_prior_auth_requirements.data, status=status.HTTP_200_OK)
        return Response(request_new_prior_auth_requirements.errors, status=status.HTTP_400_BAD_REQUEST)

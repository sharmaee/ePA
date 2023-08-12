from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from portal.api.utils import send_new_request_notification

from .serializers import (
    PriorAuthRequirementSerializer,
    AvailableSearchOptionsSerializer,
    PriorAuthRequirementDetailSerializer,
    RequestNewPriorAuthRequirementsSerializer,
    MemberDetailsSerializer,
)
from portal.logic.search.search_requirements import run_search, get_available_search_options
from portal.models import PriorAuthRequirement


class PriorAuthRequirementsView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        available_providers = get_available_search_options()
        result = AvailableSearchOptionsSerializer(available_providers).data
        return Response(result, status=status.HTTP_200_OK)


class PriorAuthRequirementSearchView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        requirements = run_search(request.data)
        result = PriorAuthRequirementSerializer(requirements, many=True).data
        return Response(result, status=status.HTTP_200_OK)


class PriorAuthRequirementDetailView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request, url_slug):
        try:
            requirement = PriorAuthRequirementDetailSerializer(PriorAuthRequirement.objects.get(url_slug=url_slug)).data
        except PriorAuthRequirement.DoesNotExist:
            requirement = None
        return Response(requirement, status=status.HTTP_200_OK)


class RequestNewPriorAuthRequirementsView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        member_details = MemberDetailsSerializer(data=request.data)
        if member_details.is_valid(raise_exception=True):
            member_details.save()
            request_new_prior_auth_requirements = RequestNewPriorAuthRequirementsSerializer(
                data=request.data, partial=True
            )
            if request_new_prior_auth_requirements.is_valid(raise_exception=True):
                request_new_prior_auth_requirements.save(member_details=member_details.instance)
                send_new_request_notification(request_new_prior_auth_requirements.instance)
                return Response(request_new_prior_auth_requirements.data, status=status.HTTP_200_OK)
        return Response(request_new_prior_auth_requirements.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView


from .serializers import (
    PriorAuthRequirementSerializer,
    AvailableSearchOptionsSerializer,
    PriorAuthRequirementDetailSerializer,
    RequestNewPriorAuthRequirementsSerializer,
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


class RequestNewPriorAuthRequirementsView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RequestNewPriorAuthRequirementsSerializer
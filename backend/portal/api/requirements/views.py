from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from portal.exceptions import PortalException

from .serializers import PriorAuthRequirementSerializer
from portal.models import PriorAuthRequirement
from portal.logic.search.search_requirements import run_search


class PriorAuthRequirementsView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        requirements = PriorAuthRequirement.objects.all()
        result = PriorAuthRequirementSerializer(requirements, many=True).data
        return Response(result, status=status.HTTP_200_OK)


class PriorAuthRequirementSearchView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        requirements = run_search(request.data)
        result = PriorAuthRequirementSerializer(requirements, many=True).data
        return Response(result, status=status.HTTP_200_OK)

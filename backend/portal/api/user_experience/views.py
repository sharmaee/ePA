from rest_framework import status
from rest_framework.response import Response

from portal.api.utils import SecuredAPIView
from .serializers import UXFeedbackSerializer
from portal.models.requirements import PriorAuthRequirement


class LeaveUXFeedbackView(SecuredAPIView):
    def post(self, request):
        url_slug = request.data.get("prior_auth_requirements", None)
        prior_auth_requirements = None
        if url_slug:
            prior_auth_requirements = PriorAuthRequirement.objects.filter(url_slug=url_slug).first()
        serializer = UXFeedbackSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(prior_auth_requirements=prior_auth_requirements, user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

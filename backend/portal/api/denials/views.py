from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from portal.utils.email_templates import send_denial_notification

from .serializers import PriorAuthDenialSerializer
from portal.api.requirements.serializers import MemberDetailsSerializer


class SubmitDenialView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        member_details = MemberDetailsSerializer(data=request.data)
        if member_details.is_valid(raise_exception=True):
            member_details.save()
            pa_denial_serializer = PriorAuthDenialSerializer(data=request.data, partial=True)
            if pa_denial_serializer.is_valid(raise_exception=True):
                pa_denial_serializer.save(member_details=member_details.instance)
                send_denial_notification(pa_denial_serializer.instance)
                return Response(pa_denial_serializer.data, status=status.HTTP_200_OK)
        return Response(pa_denial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

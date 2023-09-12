from rest_framework import status
from rest_framework.response import Response
from portal.utils.send_emails import send_service_email, NotificationType

from .serializers import PriorAuthDenialSerializer
from portal.api.requirements.serializers import MemberDetailsSerializer
from portal.api.utils import SecuredAPIView


class SubmitDenialView(SecuredAPIView):
    def post(self, request):
        member_details = MemberDetailsSerializer(data=self.request.data)
        if member_details.is_valid(raise_exception=True):
            member_details.save()
            pa_denial_serializer = PriorAuthDenialSerializer(data=self.request.data, partial=True)
            if pa_denial_serializer.is_valid(raise_exception=True):
                pa_denial_serializer.save(member_details=member_details.instance, user=self.request.user)
                send_service_email(
                    NotificationType.DENIAL.name,
                    pa_denial_serializer.instance.medication,
                    pa_denial_serializer.instance.member_details.cover_my_meds_key,
                    pa_denial_serializer.instance.release_version,
                    pa_denial_serializer.instance.submission_date,
                )
                return Response(pa_denial_serializer.data, status=status.HTTP_200_OK)
        return Response(pa_denial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

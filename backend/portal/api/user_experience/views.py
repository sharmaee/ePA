from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class PostUserExperienceView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        # TODO
        # create UserExperience object
        return Response({}, status=status.HTTP_200_OK)


class RequestUnavailableRequirementsView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        # TODO
        # create RequestUnavailableRequirements object
        # send email notification
        return Response({}, status=status.HTTP_200_OK)

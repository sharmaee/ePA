from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import UXFeedbackSerializer, RequestUnavailableRequirementsSerializer


class LeaveUXFeedbackView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UXFeedbackSerializer


class RequestUnavailableRequirementsView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RequestUnavailableRequirementsSerializer

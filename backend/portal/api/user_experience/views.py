from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import UXFeedbackSerializer, RequestNewRequirementsSerializer


class LeaveUXFeedbackView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UXFeedbackSerializer

class RequestNewRequirementsView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RequestNewRequirementsSerializer
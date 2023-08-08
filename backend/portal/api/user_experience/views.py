from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import UXFeedbackSerializer


class LeaveUXFeedbackView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UXFeedbackSerializer


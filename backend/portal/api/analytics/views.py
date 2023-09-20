from portal.api.utils import SecuredCreateAPIView

from portal.api.analytics.serializers import RequirementsSearchActionSerializer
from portal.models.analytics import RequirementsSearchAction


class AnalyticsLogViewBase(SecuredCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RequirementsSearchActionView(AnalyticsLogViewBase):
    serializer_class = RequirementsSearchActionSerializer
    queryset = RequirementsSearchAction.objects.all()

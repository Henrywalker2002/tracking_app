from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework import mixins, response, status
from time_tracking.serializers.history import HistoryDetailSerializer, HistorySummarySerializer
from time_tracking.models.history import History
from time_tracking.custom_permission import TimeTrackingPermission


class HistoryViewOnly(GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):

    serializer_class = {"retrieve" : HistoryDetailSerializer, "default" : HistorySummarySerializer}
    queryset = History.objects.all()
    permission_classes = [TimeTrackingPermission]
    filterset_fields = ['time_tracking_id']
    
    def get_serializer_class(self):
        if self.action in self.serializer_class.keys():
            return self.serializer_class[self.action]
        return self.serializer_class['default']
    
    
    
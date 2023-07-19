from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from base.views import GetByTimeTrackingIdMixin, GetByUserIdMixin
from rest_framework import mixins
from time_tracking.serializers.history import ReadHistorySerializer
from time_tracking.models.history import History
from time_tracking.custom_permission import TimeTrackingPermission

class HistoryViewOnly(GenericViewSet, mixins.RetrieveModelMixin, GetByTimeTrackingIdMixin, GetByUserIdMixin):

    serializer_class = ReadHistorySerializer
    queryset = History.objects.all()
    permission_classes = [TimeTrackingPermission]
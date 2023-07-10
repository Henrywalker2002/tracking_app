from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from base.views import GetByTimeTrackingIdMixin, GetByUserIdMixin
from rest_framework import mixins
from time_tracking.serializers.history import ReadHistorySerializer
from time_tracking.models.history import History


class HistoryViewOnly(GenericViewSet, mixins.RetrieveModelMixin, GetByTimeTrackingIdMixin, GetByUserIdMixin):

    serializer_class = ReadHistorySerializer
    queryset = History.objects.all()

from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from base.views import GetByTimeTrackingIdMixin, GetByUserIdMixin
from rest_framework import mixins
from time_tracking.serializers.subcriber import SubcriberSerializer
from time_tracking.models.subcriber import Subcriber


class SubcriberModelViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                            GetByTimeTrackingIdMixin, GetByUserIdMixin):

    serializer_class = SubcriberSerializer
    queryset = Subcriber.objects.all()

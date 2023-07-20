from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from base.views import GetByTimeTrackingIdMixin, GetByUserIdMixin
from rest_framework import mixins
from time_tracking.serializers.subcriber import WriteSubcriberSerializer, ReadSubcriberSerializer
from time_tracking.models.subcriber import Subcriber
from time_tracking.custom_permission import TimeTrackingPermission


class SubcriberModelViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                            GetByTimeTrackingIdMixin, GetByUserIdMixin):
    
    serializer_class = {"default" : WriteSubcriberSerializer, "list" : ReadSubcriberSerializer, 
                          "retrieve" : ReadSubcriberSerializer}
    queryset = Subcriber.objects.all()
    permission_classes = [TimeTrackingPermission]
    
    def get_serializer_class(self):
        if self.action in self.serializer_class.keys():
            return self.serializer_class[self.action]
        return self.serializer_class['default']
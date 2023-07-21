from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework import mixins, response, status
from time_tracking.serializers.subcriber import WriteSubcriberSerializer, ReadSubcriberSerializer
from time_tracking.models.subcriber import Subcriber
from time_tracking.custom_permission import TimeTrackingPermission
from django.http import Http404


class SubcriberModelViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin, 
                            mixins.ListModelMixin):
    
    serializer_class = {"default" : WriteSubcriberSerializer, "list" : ReadSubcriberSerializer, 
                          "retrieve" : ReadSubcriberSerializer}
    queryset = Subcriber.objects.all()
    permission_classes = [TimeTrackingPermission]
    filterset_fields = ['user_id', 'time_tracking_id', 'release_id']
    
    def get_serializer_class(self):
        if self.action in self.serializer_class.keys():
            return self.serializer_class[self.action]
        return self.serializer_class['default']
    
    def list(self, request, *args, **kwargs):
        param = request.GET 
        if 'user_id' not in param.keys() and 'time_tracking_id' not in param.keys() and 'release_id' not in param.keys():
            raise Http404
        return super().list(request, *args, **kwargs)
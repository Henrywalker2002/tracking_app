from time_tracking.models import Subcriber
from notification.models import Notification
from notification.serializers import ReadSummaryNotificationSerializer, ReadDetailNotificationSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from notification.custom_permission import NotificationPermission
from rest_framework import status
    
    
class NotificationViewset(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    
    queryset = Notification.objects.all()
    permission_classes = [NotificationPermission]
    filterset_fields = ['user_id', "checked", "type"]
    serializer_class = {"list" : ReadSummaryNotificationSerializer, "default" : ReadDetailNotificationSerializer}
    
    def get_serializer_class(self):
        if self.action in self.serializer_class.keys():
            return self.serializer_class[self.action]
        return self.serializer_class['default']
    
    def get_queryset(self):
        if self.action == "list":
            return Notification.objects.select_related('user').order_by('-created_at')
        return self.queryset
        
    def list(self, request, *args, **kwargs):
        param = request.GET
        if "user_id" not in param.keys():
            return Response({"detail" : "Not found"}, status= status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)
    
    @action(detail= True, url_path= 'checked', methods= ['put'])
    def checked(self, request, pk):
        instance = self.get_object()
        instance.checked = True
        instance.save()
        return Response(self.get_serializer(instance).data)

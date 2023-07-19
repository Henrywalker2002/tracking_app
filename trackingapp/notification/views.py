from time_tracking.models import Subcriber
from base.views import GetByUserIdMixin
from notification.models import Notification
from notification.serializers import ReadNotificationSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from notification.custom_permission import NotificationPermission
    
    
class NotificationViewset(GenericViewSet, RetrieveModelMixin, GetByUserIdMixin):
    
    queryset = Notification.objects.all()
    serializer_class = ReadNotificationSerializer
    permission_classes = [NotificationPermission]
    
    def get_queryset(self):
        if self.action == "list":
            return Notification.objects.select_related('user')
        return self.queryset
        
    
    @action(detail= True, url_path= 'checked', methods= ['put'])
    def checked(self, request, pk):
        instance = self.get_object()
        instance.checked = True
        instance.save()
        return Response(self.get_serializer(instance).data)

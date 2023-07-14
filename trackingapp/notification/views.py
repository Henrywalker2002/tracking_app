from time_tracking.models import Subcriber
from base.views import GetByUserIdMixin
from notification.models import Notification
from notification.serializers import ReadNotificationSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
    
    
class NotificationViewset(GenericViewSet, RetrieveModelMixin, GetByUserIdMixin):
    
    queryset = Notification.objects.all()
    serializer_class = ReadNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail= True, url_path= 'checked', methods= ['put'])
    def checked(self, request, pk):
        instance = self.get_object()
        instance.checked = True
        instance.save()
        return Response(self.get_serializer(instance).data)

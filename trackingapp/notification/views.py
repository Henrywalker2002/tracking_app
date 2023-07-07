from time_tracking.models import Subcriber
from base.views import GetByUserIdMixin
from notification.models import Notification
from notification.serializers import ReadNotificationSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from media.views import process_add_to_media
from base.task_queue import add_to_queue

@add_to_queue
def proccess_history_change(history_instance):
    """
    Add notification for user who subcribed time tracking
    """
    user_lst = Subcriber.objects.filter(
            time_tracking_id=history_instance.time_tracking_id).values_list('user', flat = True)
    data_lst = [{"user_id": user, "object_id": history_instance.id,
                 "type": 'TIME_TRACKING_HISTORY'} for user in user_lst]
    instance_lst = [Notification(**data) for data in data_lst]
    Notification.objects.bulk_create(instance_lst) 
    process_add_to_media(history_instance)
    
    
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
    

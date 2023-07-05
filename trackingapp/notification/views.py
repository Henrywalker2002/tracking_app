from rest_framework import viewsets
from time_tracking.models import Subcriber
from base.views import BulkCreateMixin
import threading
from notification.models import Notification


def proccess_history_change(history_instance, user):
    user_lst = Subcriber.objects.filter(
            time_tracking_id=history_instance.time_tracking_id).values_list('user', flat = True)
    data_lst = [{"user_id": user, "object_id": history_instance.id,
                 "type": 'TIME_TRACKING_HISTORY'} for user in user_lst]
    instance_lst = [Notification(**data) for data in data_lst]
    Notification.objects.bulk_create(instance_lst) 

class NotificationViewset(viewsets.ReadOnlyModelViewSet, BulkCreateMixin):
    pass 

        

from notification.models import Notification
from media.execute import process_add_to_media
from admin_app.task_queue import add_to_queue

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
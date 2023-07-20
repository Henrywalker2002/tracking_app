from notification.models import Notification, TypeNotification
from time_tracking.models.subcriber import Subcriber, SubcriberType
from admin_app.task_queue import add_to_queue


def add_notification_for_history_change(history_instance):
    """
    Add notification for user who subcribed time tracking
    """
    user_lst = Subcriber.objects.filter(
        time_tracking_id=history_instance.time_tracking_id).values_list('user', flat=True)
    data_lst = [{"user_id": user, "object_id": history_instance.id,
                 "type": 'TIME_TRACKING_HISTORY'} for user in user_lst]
    instance_lst = [Notification(**data) for data in data_lst]
    Notification.objects.bulk_create(instance_lst)


def add_notification_for_release(tasks):
    """
    Input: List of task which is over deadline 
    => add notification for who subcriber release
    """
    instance_lst = []
    temp_cache = {}
    for task in tasks:
        release_id = task.release_id
        if release_id in temp_cache.keys():
            user_lst = temp_cache.get('release_id')
        else:
            user_lst = Subcriber.objects.filter(
                object_type=SubcriberType.RELEASE, release_id=release_id).values_list('user_id', flat=True)
        instance_lst += [Notification(object_id=task.id, user_id=user_id,
                                      type=TypeNotification.WORK_FLOW) for user_id in user_lst]
    Notification.objects.bulk_create(instance_lst)

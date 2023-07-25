from django.utils import timezone
from time_tracking.models.time_tracking import TimeTracking, StatusTimeTracking
from notification.execute import add_notification_for_release
import schedule
import time
from admin_app.task_queue import add_to_queue
from time_tracking.models.history import History
from time_tracking.models.subcriber import Subcriber, SubcriberType
from notification.execute import add_notification_for_history_change


def check_task_over_deadline():
    """
    List of task which over deadline and notify to user who subcriber to task's release everyday
    """
    def inner():
        expired_task = TimeTracking.objects.filter(
            end_time__lte = timezone.now()).exclude(status=StatusTimeTracking.DONE)
        add_notification_for_release(expired_task)
    
    inner()
    
    schedule.every().day.at("00:00").do(inner)
    
    while True:
        schedule.run_pending()
        time.sleep(1)


@add_to_queue
def process_history(current_time_tracking, old_instance, new_instance):
    excluded_fields = ['id', 'created_at',
                       'modified_at', 'created_by', 'updated_by']
    change_lst = {}
    for key in old_instance.keys():
        if key in excluded_fields:
            continue
        if old_instance[key] != new_instance[key]:
            if key == 'user':
                # user handle 
                subcriber_instance = Subcriber.objects.filter(user_id=old_instance.get('user_id'), 
                                    time_tracking_id=old_instance.get('id'), object_type = SubcriberType.TASK)
                change_lst[key] = {"old_value": str(old_instance[key].get('id')), "new_value": str(new_instance[key].get('id'))}
                
                if subcriber_instance:
                    subcriber_instance.delete()
                continue 
            elif key == "release":
                change_lst[key] = {"old_value" : str(old_instance[key].get('id')), "new_value" : str(new_instance[key].get('id'))}
                continue
            change_lst[key] = {"old_value": str(old_instance[key]), "new_value": str(new_instance[key])}
            
    history_data = {"time_tracking": current_time_tracking,
                    "change_detection": change_lst}
    if change_lst:
        history_instance = History.objects.create(**history_data)
        add_notification_for_history_change(history_instance) 
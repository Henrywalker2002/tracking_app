from django.utils import timezone
from time_tracking.models.time_tracking import TimeTracking, StatusTimeTracking
from notification.execute import add_notification_for_release
import schedule
import time


def check_task_over_deadline():
    """
    List of task which over deadline and notify to user who subcriber to task's release everyday
    """
    def inner():
        expired_task = TimeTracking.objects.filter(
            end_time__lte = timezone.now()).exclude(status=StatusTimeTracking.DONE)
        add_notification_for_release(expired_task)
    
    schedule.every().day.at("00:00").do(inner)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

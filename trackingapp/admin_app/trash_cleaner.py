from time_tracking.models.time_tracking import TimeTracking
from time_tracking.models.release import Release
from time_tracking.models.history import History
from user.models import ResetCodeUser
import schedule
import time
from django.core import management
from datetime import timedelta
from django.utils import timezone
import threading

def delete_time_tracking_and_release():
    release_instances = Release.objects.filter(is_deleted = True)
    release_instances.delete()
    time_tracking_instances = TimeTracking.objects.filter(is_deleted=True)
    time_tracking_instances.delete()

def session_clean_up():
    management.call_command("clearsessions")

def clear_history_time_tracking():
    old_history = History.objects.filter(created_at__lte = timezone.now() - timedelta(days= 30))
    old_history.delete()
    
def clear_expired_code():
    instance_lst = ResetCodeUser.objects.filter(expired_time__lt = timezone.now())
    instance_lst.delete()

def auto_run_clean():
    def run_all():
        delete_time_tracking_and_release()
        session_clean_up()
        clear_history_time_tracking()
        clear_expired_code()
        
    schedule.every().day.at('00:00').do(run_all)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

    
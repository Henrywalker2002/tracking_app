from django.apps import AppConfig
import threading
import schedule
import time


class TimeTrackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'time_tracking'

    def ready(self):
        """
        Custom to add auto delete 
        """
        time_tracking_model = self.get_model('timetracking', require_ready=True)
        release_model = self.get_model('release', require_ready= True)
        thread = threading.Thread(
            target=self.proccess_auto_delete, args=(time_tracking_model, release_model ), daemon=True)
        thread.start()

    def proccess_auto_delete(self, time_tracking_model, release_model):
        def delete(time_tracking_model, release_model):
            release_instances = release_model.objects.filter(is_deleted = True)
            release_instances.delete()
            time_tracking_instances = time_tracking_model.objects.filter(is_deleted=True)
            time_tracking_instances.delete()
            
        schedule.every(60).minutes.do(delete, time_tracking_model, release_model)

        while True:
            schedule.run_pending()
            time.sleep(1)

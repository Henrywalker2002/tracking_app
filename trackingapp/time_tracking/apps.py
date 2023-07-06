from django.apps import AppConfig
import threading
import schedule
import time


class TimeTrackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'time_tracking'

    def ready(self):
        model = self.get_model('timetracking', require_ready=True)
        thread = threading.Thread(
            target=self.proccess_auto_delete, args=(model, ), daemon=True)
        thread.start()

    def proccess_auto_delete(self, model):
        def delete(model):
            instance_lst = model.objects.filter(is_deleted=True)
            instance_lst.delete()

        schedule.every(60).minutes.do(delete, model)

        while True:
            schedule.run_pending()
            time.sleep(1)

from django.apps import AppConfig
from admin_app.task_queue import proccess_task_queue
import threading

class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_app'

    def ready(self):
        thread_process_task = threading.Thread(target= proccess_task_queue, args=(), daemon= True)
        thread_process_task.start()
        
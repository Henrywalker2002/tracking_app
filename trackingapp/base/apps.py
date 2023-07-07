from django.apps import AppConfig
from base.task_queue import proccess_task_queue
import threading

class BaseappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

    def ready(self):
        thread_process_task = threading.Thread(target= proccess_task_queue, args=(), daemon= True)
        thread_process_task.start()
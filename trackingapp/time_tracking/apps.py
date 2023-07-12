from django.apps import AppConfig
import threading
import schedule
import time


class TimeTrackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'time_tracking'

from django.apps import AppConfig
from trackingapp.custom_middleware import taskQueue

class MediaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'media'
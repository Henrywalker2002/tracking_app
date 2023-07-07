from django.apps import AppConfig
from threading import Thread
import schedule
import time

class MediaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'media'
    
    def ready(self):

        thread = Thread(target= self.send_mail, args= (), daemon= True)
        thread.start()
    
    def send_mail(self):
        from media.views import send_all_mail
        schedule.every(5).minutes.do(send_all_mail)
        
        while True:
            schedule.run_pending()
            time.sleep(1)
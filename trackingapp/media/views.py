from media.models import Media
from media.serializers import ReadMediaSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from django.template.loader import get_template
from rest_framework.response import Response
from django.core.mail import send_mail, EmailMessage
from django.core import mail
from django.conf import settings
from smtplib import SMTPException
from functools import reduce

def process_add_to_media(history_instance, media_to = None):
    media_to = media_to or "hung.nguyen0304@hcmut.edu.vn"
    media_from = settings.EMAIL_HOST_USER
    dic = {"data" : history_instance.change_detection, "time" : history_instance.created_at}
    htmly = get_template('notification.html')
    content = htmly.render(dic)
    
    media = Media.objects.create(media_from=media_from, media_to=media_to, content=content, 
                         context_type= 'HTML', sending_method="EMAIL")
        
def send_all_mail():
    error_ids = []
    success_ids = []
    instance_lst = Media.objects.filter(status = "IN_QUEUE")
    connection = mail.get_connection()
    connection.open()
    for instance in instance_lst:
        
        instance.status = "IN_PROGRESS"
        instance.save()
        
        email = EmailMessage(subject= "notification", body= instance.content, 
                             from_email= instance.media_from, to = [instance.media_to])
        if instance.context_type == "HTML":
            email.content_subtype = 'html'
            
        try:
            connection.send_messages([email])
            instance.status = "SUCCESS"
            instance.save()
            success_ids.append(instance.id)
        except SMTPException as e:
            instance.retry_count += 1
            instance.status = "FAIL"
            instance.save()
            error_ids.append(instance.id)
            
    connection.close()
    
class MediaViewSet(GenericViewSet, ListModelMixin):
    
    queryset = Media.objects.all()
    serializer_class = ReadMediaSerializer
    
from media.models import Media, MediaStatusChoices, SendMethodChoices, ContentTypeChoices
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.core import mail
from django.conf import settings
from smtplib import SMTPException
from functools import reduce
from django.db.models import Q
import logging


def send_all_mail():

    error_ids = []
    success_ids = []
    # get in queue and fail not retry > 3
    instance_lst = Media.objects.filter(Q(status=MediaStatusChoices.IN_QUEUE) 
                                        | (Q(status=MediaStatusChoices.FAIL) & Q(retry_count__lt = 3)) 
                                        & Q(sending_method = SendMethodChoices.EMAIL))
    connection = mail.get_connection()
    connection.open()
    for instance in instance_lst:

        instance.status = MediaStatusChoices.IN_PROCESS
        instance.save()

        email = EmailMessage(subject="notification", body=instance.content,
                             from_email=instance.media_from, to=[instance.media_to])
        if instance.context_type == ContentTypeChoices.HTML:
            email.content_subtype = 'html'

        try:
            connection.send_messages([email])
            instance.status = MediaStatusChoices.SUCCESS
            instance.save()
            success_ids.append(instance.id)
        except SMTPException as e:
            instance.retry_count += 1
            instance.status = MediaStatusChoices.FAIL
            instance.save()
            error_ids.append(instance.id)
    logging.info(f"send mail success {success_ids} error {error_ids}")

    connection.close()

def send_code(code, email):
    dic = {"code" : code}
    htmly = get_template('send_new_password.html')
    body = htmly.render(dic)
    msg = EmailMessage("reset password", body, settings.EMAIL_HOST_USER, [email])
    msg.content_subtype = 'html'
    msg.send(fail_silently= True)
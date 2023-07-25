from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.core import mail
from django.conf import settings
from smtplib import SMTPException
from admin_app.task_queue import add_to_queue


@add_to_queue
def send_reset_password_code(code, email):
    dic = {"code" : code}
    htmly = get_template('send_reset_code.html')
    body = htmly.render(dic)
    msg = EmailMessage("reset password", body, settings.EMAIL_HOST_USER, [email])
    msg.content_subtype = 'html'
    msg.send(fail_silently= True)
    
@add_to_queue
def send_new_password(password, email):
    dic = {"password" : password}
    htmly = get_template('send_new_password.html')
    body = htmly.render(dic)
    msg = EmailMessage("welcome to our system", body, settings.EMAIL_HOST_USER, [email])
    msg.content_subtype = 'html'
    msg.send(fail_silently= True)
    
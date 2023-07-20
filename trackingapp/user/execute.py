from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.core import mail
from django.conf import settings
from smtplib import SMTPException


def send_code(code, email):
    dic = {"code" : code}
    htmly = get_template('send_new_password.html')
    body = htmly.render(dic)
    msg = EmailMessage("reset password", body, settings.EMAIL_HOST_USER, [email])
    msg.content_subtype = 'html'
    msg.send(fail_silently= True)
from django.core.mail import send_mail
from django.conf import settings
from celery import Celery

app = Celery('news_blog', broker='pyamqp://guest@localhost//')


@app.task
def send_email(mail_subject, message, to_email):
    print(app.task)
    return send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email, ])

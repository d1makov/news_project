from django.core.mail import send_mail
from django.conf import settings
from news_blog.celery import app


@app.task
def send_email(mail_subject, message, to_email):
    send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email, ])

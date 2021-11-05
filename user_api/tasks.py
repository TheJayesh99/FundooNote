from email.message import EmailMessage
from celery import shared_task
from user_api.models import User
from user_api.serializers import UserSerializer
import smtplib
import os

from dotenv import load_dotenv

load_dotenv(".env")

@shared_task(bind=True)
def send_emails(self):

    user_list = User.objects.filter(is_mail_sent=False)
    for user in user_list:
        if user.is_verified:
            subject = 'welcome to FundooNotes'
            message = f'Hi {user.username}, Thanks you for joining our FundooNotes'
            msg = EmailMessage()
            msg.set_content(message)
            msg['From'] = os.getenv('EMAIL_HOST_USER')
            msg['To'] = user.email
            msg['Subject'] = subject
            server = smtplib.SMTP('smtp.gmail.com', 587)  
            # start TLS for security
            server.starttls() 
            # Authentication
            server.login(os.getenv('EMAIL_HOST_USER'), os.getenv('EMAIL_PASSWORD'))
            # sending the mail
            server.send_message(msg=msg)
            # terminating the session
            server.quit() 
            user.is_mail_sent = True
            user.save()  

    print("send mail")


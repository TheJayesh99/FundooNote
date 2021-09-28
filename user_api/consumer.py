import json
import os
import smtplib
import sys
from email.message import EmailMessage

import pika
from dotenv import load_dotenv

load_dotenv(".env")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        mail_data=json.loads(body)
        subject = 'welcome to FundooNotes'
        message = f'Hi {mail_data.get("username")}, thank you for registering in FundooNotes. click on the link below to get yourself verified\n http://127.0.0.1:8000/user/verify/{mail_data.get("encoded_token")}/'
        msg = EmailMessage()
        msg.set_content(message)
        msg['From'] = mail_data.get("sender")
        msg['To'] = mail_data.get("email")
        msg['Subject'] = subject
        server = smtplib.SMTP('smtp.gmail.com', 587)  
        # start TLS for security
        server.starttls() 
        # Authentication
        server.login(mail_data.get("sender"), os.getenv('EMAIL_PASSWORD'))
        # sending the mail
        server.send_message(msg=msg)
        # terminating the session
        server.quit()   

    channel.basic_consume(queue='send_mail', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

from dotenv import load_dotenv
import smtplib
import yaml 
import os
import json

load_dotenv()


smtp_server = os.environ['smtp_server']
smtp_port = os.environ['smtp_port']
sender_email = os.environ['sender_email']
app_password = os.environ['app_password']

def load_config(path):
    with open(path , 'r') as fp:
        data = yaml.safe_load(fp) 
    return data  


def send_mail(receiver_email_id):
    s = smtplib.SMTP(smtp_server, 587)
    s.starttls()
    s.login(sender_email , app_password)
    message = "Thank you for reaching out, your resume is being processed"
    s.sendmail(sender_email, receiver_email_id, message)
    s.quit()

# if __name__ == "__main__":
#     send_mail("ayush89718@gmail.com")

import email
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import datetime

load_dotenv()

def getHeader():
    return {
        "Authorization": "Bearer " + os.getenv('TOKEN'),
        "Content-Type": "application/json",
        "Notion-Version": "2021-08-16"
    }

def isTestMode():
    return os.getenv('TESTMODE') == 'ON'

def getInsertToNotion():
    return os.getenv('INSERT_TO_NOTION') == 'TRUE'

def getSendEmails():
    return os.getenv('SEND_EMAILS') == 'TRUE'

def sendEmail(subject, body):
    print('Sending Email')
    emailAddress = os.getenv('EMAIL_ADDRESS')
    emailPassword = os.getenv('EMAIL_PASSWORD')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = emailAddress
    msg['To'] = emailAddress
    msg.add_alternative(body, subtype='html')

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(emailAddress, emailPassword)

        message = f'Subject: { subject }\n\n{ body }'

        smtp.send_message(msg)
        print('Email Sent')
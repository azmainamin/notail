import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

from .IEmailSender import IEmailSender
from Constants import FILETYPES

class EmailSender(IEmailSender):
    def __init__(self, emailType):
        self.to_id = os.getenv('TO')
        self.from_id = os.getenv('FROM')
        self.pw = os.getenv('PW')
        self.emailType = emailType

    def sendEmail(self, emailBody):
        """
        Send a html email with the emailBody
        """
        message = self._createMessageObject()
        messageBody = MIMEText(emailBody, FILETYPES['html'])
        message.attach(messageBody)

        self._send(message)
    
    def _createMessageObject(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = "You got some learning to do."
        message["From"] = self.from_id
        message["To"] = self.to_id

        return message

    def _send(self, email):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.from_id, self.pw)
            server.sendmail(self.from_id, self.to_id, email.as_string())
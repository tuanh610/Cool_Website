import base64
import mimetypes
import pickle
import os.path
from email import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEBase, MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
import os


"""
In order to get the crednetials.json file please follow this links 
https://developers.google.com/gmail/api/quickstart/python?authuser=1
"""
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

class mailModule:
    def getCredential(self):
        creds = None
        base = os.path.dirname(os.path.realpath(__file__)) + '/..'
        tokenPath = base + "/token.pickle"
        credPath = base + "/credentials.json"
        if os.path.exists(tokenPath):
            with open(tokenPath, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credPath, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(tokenPath, 'wb') as token:
                pickle.dump(creds, token)
        service = build('gmail', 'v1', credentials=creds)
        return service

    def create_message(self, sender, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        temp = message.as_string()
        return {'raw': base64.urlsafe_b64encode(temp.encode('UTF-8')).decode('ascii')}


    def create_message_with_attachment(self, sender, to, subject, message_text, file):
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        msg = MIMEText(message_text)
        message.attach(msg)

        content_type, encoding = mimetypes.guess_type(file)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(file, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(file, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(file, 'rb')
            msg = MIMEAudio(file, _subtype=sub_type)
            fp.close()
        else:
            fp = open(file, 'rb')
            msg = MIMEBase(file, _subtype=sub_type)
            fp.close()
        filename = os.path.basename(file)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}

    def send_message(self, service, message, user_id="me"):
        try:
            msg = (service.users().messages().send(userId=user_id, body=message).execute())
            print("Message Id: %s" % msg['id'])
            return msg
        except errors.HttpError as error:
            print("Error occurred: %s" % error)
            return None



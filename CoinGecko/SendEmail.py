import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient import errors, discovery
from oauth2client import client

import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase

SCOPES = ["https://mail.google.com/"]
# CLIENT_SECRET_FILE = home+'credentials.json'
# APPLICATION_NAME = 'Gmail API Python Send Email'


def get_credentials():
    client_id = (
        "304284658334-i3vhdl4lb124n3lie60u0oi31clcahgh.apps.googleusercontent.com"
    )
    client_secret = "lBq6AVgs689i_4M00lRmTG0s"
    refresh_token = "1//0gH5r995WQwtsCgYIARAAGBASNwF-L9IrV8UiW8S4i2xQ521Lap4N2rAtDlJ0EbMQ3vRd1mUqThS6SIHoKxfVlRfY9045qEvtXZY"
    creds = client.GoogleCredentials(
        None,
        client_id,
        client_secret,
        refresh_token,
        None,
        "https://accounts.google.com/o/oauth2/token",
        "my-user-agent",
    )
    return creds


def SendMessage(sender, to, subject, msgHtml, msgPlain, attachmentFile=None):
    credentials = get_credentials()
    service = discovery.build(
        "gmail", "v1", credentials=credentials, cache_discovery=False
    )
    if attachmentFile:
        message1 = createMessageWithAttachment(
            sender, to, subject, msgPlain, attachmentFile
        )
    else:
        message1 = CreateMessageHtml(sender, to, subject, msgHtml, msgPlain)
    result = SendMessageInternal(service, "me", message1)
    return result


def SendMessageInternal(service, user_id, message):
    try:
        message = (
            service.users().messages().send(userId=user_id, body=message).execute()
        )
        print("Message Id: %s" % message["id"])
        return message
    except errors.HttpError as error:
        print("An error occurred: %s" % error)
        return "Error"


def CreateMessageHtml(sender, to, subject, msgHtml, msgPlain):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to
    if msgPlain:
        msg.attach(MIMEText(msgPlain, "plain"))
    if msgHtml:
        msg.attach(MIMEText(msgHtml, "html"))
    return {
        "raw": base64.urlsafe_b64encode(msg.as_string().encode("utf-8")).decode("ascii")
    }


def createMessageWithAttachment(sender, to, subject, message_text, file):

    message = MIMEMultipart()
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = "application/octet-stream"
    main_type, sub_type = content_type.split("/", 1)
    print(content_type)
    if main_type == "text":
        fp = open(file, "r")
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == "image":
        fp = open(file, "rb")  # type: ignore
        msg = MIMEImage(fp.read(), _subtype=sub_type)  # type: ignore
        fp.close()
    elif main_type == "audio":
        fp = open(file, "rb")  # type: ignore
        msg = MIMEAudio(fp.read(), _subtype=sub_type)  # type: ignore
        fp.close()
    else:
        fp = open(file, "rb")  # type: ignore
        msg = MIMEBase(main_type, sub_type)  # type: ignore
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(file)
    msg.add_header("Content-Disposition", "attachment", filename=filename)
    message.attach(msg)

    return {
        "raw": base64.urlsafe_b64encode(message.as_string().encode("utf-8")).decode(
            "ascii"
        )
    }


def send_html_notification_email(recipient, subject, msg):
    to = recipient
    sender = "technology@jstcap.com"
    sub = subject
    msgHtml = msg
    msgPlain = ""
    SendMessage(sender, to, sub, msgHtml, msgPlain)


def send_notification_email(recipient, subject, msg):
    to = recipient
    sender = "deepa@jstdigitaltrading.com"
    sub = subject
    msgHtml = ""
    msgPlain = msg
    SendMessage(sender, to, sub, msgHtml, msgPlain)


def send_notification_email_with_file(recipient, subject, msg, att):
    to = recipient
    sender = "technology@jstcap.com"
    sub = subject
    msgHtml = ""
    msgPlain = msg
    SendMessage(sender, to, sub, msgHtml, msgPlain, attachmentFile=att)



    
    



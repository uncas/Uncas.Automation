# From: https://developers.google.com/gmail/api/quickstart/python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from Services.Google.GoogleAuth import getCredentials
from Utils.FileUtils import writeText
import json

QUERY_INBOX = "in:inbox"
QUERY_UNREAD = "is:unread"

def getInboxMessages():
  creds = getCredentials()
  try:
    service = build("gmail", "v1", credentials=creds)
    results = getMessagesInfo(service, QUERY_INBOX)
    for message in results["messages"]:
        messageId = message["id"]
        content = getMessageContent(service, messageId)
        contentText = json.dumps(content, indent = 2)
        writeText("Data/Gmail", messageId + ".json", contentText)
        payload = content["payload"]
        headers = payload["headers"]
        sender = getHeaderValue(headers, "From")
        recipient = getHeaderValue(headers, "To")
        date = getHeaderValue(headers, "Date")
        subject = getHeaderValue(headers, "Subject")
        body = getBody(payload)
        yield { "sender": sender, "recipient": recipient, "date": date, "subject": subject, "body": body }
    return
  except HttpError as err:
    print(err)

def getBody(payload):
    parts = payload["parts"]
    bodyText = []
    for part in parts:
        if part["mimeType"] == "multipart/alternative":
            for subPart in part["parts"]:
                subPartBody = getPartBody(subPart)
                if subPartBody:
                    bodyText.append(subPartBody)
        else:
            partBody = getPartBody(part)
            if partBody:
                bodyText.append(partBody)
    return "\n".join(bodyText)

def getPartBody(part):
    try:
        data = part["body"]["data"]
        import base64
        byte_code = base64.urlsafe_b64decode(data)
        return byte_code.decode("utf-8")
    except BaseException as error:
        print(error)
        return

def getHeaderValue(headers, name):
  for header in headers:
    if header["name"] == name:
      return header["value"]

def getMessagesInfo(service, query):
   return service.users().messages().list(userId="me", q=query).execute()

def getThread(service, threadId):
  return service.users().threads().get(userId = "me", id = threadId).execute()

def getMessageContent(service, messageId):
  return service.users().messages().get(userId = "me", id = messageId, format = "full").execute()
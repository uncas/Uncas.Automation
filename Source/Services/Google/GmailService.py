# From: https://developers.google.com/gmail/api/quickstart/python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from Services.Google.GoogleAuth import getCredentials

def getUnreadMessages():
  creds = getCredentials()
  try:
    service = build("gmail", "v1", credentials=creds)
    results = getUnreadMessagesInfo(service)
    for message in results["messages"]:
        messageId = message["id"]
        content = getMessageContent(service, messageId)
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
    for part in parts:
        if part["mimeType"] == "multipart/alternative":
            for subPart in part["parts"]:
                if subPart["mimeType"] == "text/plain":
                    encodedBody = subPart["body"]["data"]
                    from base64 import urlsafe_b64decode
                    return urlsafe_b64decode(encodedBody)

def getHeaderValue(headers, name):
  for header in headers:
    if header["name"] == name:
      return header["value"]

def getUnreadMessagesInfo(service):
  return service.users().messages().list(userId="me", q="is:unread").execute()

def getThread(service, threadId):
  return service.users().threads().get(userId = "me", id = threadId).execute()

def getMessageContent(service, messageId):
  return service.users().messages().get(userId = "me", id = messageId, format = "full").execute()
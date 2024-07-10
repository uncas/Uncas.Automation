# From: https://developers.google.com/gmail/api/quickstart/python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from Services.Google.GoogleAuth import getCredentials
from Utils.FileUtils import writeText
import json

QUERY_INBOX = "in:inbox"
QUERY_UNREAD = "is:unread"

creds = getCredentials()
gmailService = build("gmail", "v1", credentials=creds)

def getInboxMessages():
  try:
    results = getMessagesInfo(QUERY_INBOX)
    for message in results["messages"]:
        internalMessageId = message["id"]
        content = getMessageContent(internalMessageId)
        contentText = json.dumps(content, indent = 2)
        writeText("Data/Gmail", internalMessageId + ".json", contentText)
        payload = content["payload"]
        headers = payload["headers"]
        sender = getHeaderValue(headers, "From")
        recipient = getHeaderValue(headers, "To")
        date = getHeaderValue(headers, "Date")
        subject = getHeaderValue(headers, "Subject")
        threadId = message["threadId"]
        globalMessageId = getHeaderValue(headers, "Message-ID")
        #body = getBody(payload)
        body = parse_email_body(content)
        yield { 
          "sender": sender, 
          "recipient": recipient, 
          "date": date, 
          "subject": subject, 
          "body": body, 
          "threadId": threadId, 
          "globalMessageId": globalMessageId, 
          "internalMessageId": internalMessageId 
        }
    return
  except HttpError as err:
    print(err)

def getBody(payload):
    if "parts" not in payload:
       return ""
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

def parse_email_body(msg: dict) -> str:
    import base64
    parts = msg["payload"].get("parts", [])
    for part in parts:
        # only parse the first text/plain part, ignore the rest
        if part["mimeType"] == "text/plain":
            body = part["body"].get("data", "")
            body = base64.urlsafe_b64decode(
                body.encode("ASCII")).decode("utf-8")
            break
    else:
        body = ""

    return body

def getHeaderValue(headers, name):
  for header in headers:
    if header["name"] == name:
      return header["value"]

def getMessagesInfo(query):
  return gmailService.users().messages().list(userId = "me", q=query).execute()

def getThread(threadId):
  return gmailService.users().threads().get(userId = "me", id = threadId).execute()

def getMessageContent(internalMessageId):
  return gmailService.users().messages().get(userId = "me", id = internalMessageId, format = "full").execute()

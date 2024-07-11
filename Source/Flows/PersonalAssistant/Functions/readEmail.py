from Services.Google.GmailService import getInboxMessages
from Services.Google.GmailSendService import createDraft

def readEmail():
	messages = getInboxMessages()
	result = [{
		"sender": message["sender"], 
		"date": message["date"], 
		"subject": message["subject"], 
		"body": message["body"],
		"internalMessageId": message["internalMessageId"]
	} for message in messages]
	return result

def writeEmail(data):
	body = data["body"]
	subject = data["subject"]
	recipient = data["recipient"]
	internalMessageId = data["internalMessageId"] if "internalMessageId" in data else None
	createDraft(recipient, subject, body, internalMessageId)
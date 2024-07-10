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
	sender = data["sender"]
	recipient = data["recipient"]
	internalMessageId = data["internalMessageId"]
	createDraft(recipient, subject, body, sender, internalMessageId)
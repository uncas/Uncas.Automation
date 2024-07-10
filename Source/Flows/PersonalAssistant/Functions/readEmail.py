from Services.Google.GmailService import getInboxMessages

def readEmail():
	messages = getInboxMessages()
	result = [{"sender": message["sender"], "date": message["date"], "subject": message["subject"], "body": message["body"]} for message in messages]
	#for item in result:
	#	print(item)
	return result

def assistWithMails():
	from Services.Google.GmailService import getInboxMessages
	messages = getInboxMessages()
	for message in messages:
		print("From " + message["sender"] + ": " + message["subject"])
		#cleanBody = message["body"] #.replace('\n', ' ').replace('\r', '')
		#print(cleanBody)
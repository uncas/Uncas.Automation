# https://developers.google.com/gmail/api/guides/threads

import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from easai.Services.Google.GoogleAuth import getCredentials
from easai.Services.Google.GmailService import getMessageContent

def createDraft(recipient, subject, body, internalMessageId = None):
	print("Should I create a draft with the following parameters: " + recipient + ", " + subject)
	decision = input("y/n ")
	if (decision != "y"):
		return

	creds = getCredentials()
	try:
		service = build("gmail", "v1", credentials=creds)
		message = EmailMessage()
		message.set_content(body)
		message["To"] = recipient
		#message["From"] = sender
		if internalMessageId:
			originalMessage = getMessageContent(internalMessageId)
			message["ThreadId"] = originalMessage["threadId"]
			message['References'] = originalMessage["globalMessageId"]
			message['In-Reply-To'] = originalMessage["globalMessageId"]
			message["Subject"] = originalMessage["subject"]
		else:
			message["Subject"] = subject
		encodedMessage = base64.urlsafe_b64encode(message.as_bytes()).decode()
		createMessage = {"message": {"raw": encodedMessage}}
		draft = (
			service.users()
			.drafts()
			.create(userId="me", body=createMessage)
			.execute()
		)
		return draft
	except HttpError as error:
		print(f"An error occurred: {error}")
		return None

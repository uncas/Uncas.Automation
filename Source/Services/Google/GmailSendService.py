# https://developers.google.com/gmail/api/guides/threads

import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from Services.Google.GoogleAuth import getCredentials

def createDraft(recipient, subject, body, sender, internalMessageId = None):
	print("Should I create a draft with the following parameters: " + recipient + ", " + subject + ", " + sender)
	decision = input("y/n ")
	if (decision != "y"):
		return

	creds = getCredentials()
	try:
		service = build("gmail", "v1", credentials=creds)
		message = EmailMessage()
		message.set_content(body)
		message["To"] = recipient
		message["From"] = sender
		message["Subject"] = subject
		#if internalMessageId:
		#	message["ThreadId"] = threadId
		#	message['References'] = globalMessageId
		#	message['In-Reply-To'] = globalMessageId
		#	message["Subject"] = 
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

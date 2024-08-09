from uncas_automation.Services.Google.GmailService import getInboxMessages

def testGmailService():
	messages = getInboxMessages()
	for message in messages:
		print("From " + message["sender"] + ": " + message["subject"])
		body = message["body"]
		if body:
			print("Body: " + body[:min(len(body), 200)])
		print()

if __name__ == "__main__":
	testGmailService()
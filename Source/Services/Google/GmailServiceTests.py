from Services.Google.GmailService import getInboxMessages

def testGmailService():
	messages = getInboxMessages()
	print(list(messages))

if __name__ == "__main__":
	testGmailService()
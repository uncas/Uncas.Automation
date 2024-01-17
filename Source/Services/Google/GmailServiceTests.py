from Services.Google.GmailService import getUnreadMessages

def testGmailService():
	messages = getUnreadMessages()
	print(list(messages))

if __name__ == "__main__":
	testGmailService()
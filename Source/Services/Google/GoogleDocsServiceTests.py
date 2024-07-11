from Services.Google.GoogleDocsService import readDocument

def testGoogleDocsService():
	id = "xx"
	doc = readDocument(id)
	title = doc["title"]
	text = doc["text"]
	print("The title of the document is: " + title)
	print("The text content of the document is: " + text)

if __name__ == "__main__":
	testGoogleDocsService()
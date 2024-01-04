from Services.Google.GoogleDocsService import readDocument

def testGoogleDocsService():
	id = "1j80Lx1Rlu3w1gOh6FHZeF3TftA4vyV9VNEyskpF6wO4"
	doc = readDocument(id)
	title = doc["title"]
	text = doc["text"]
	print("The title of the document is: " + title)
	print("The text content of the document is: " + text)

if __name__ == "__main__":
	testGoogleDocsService()
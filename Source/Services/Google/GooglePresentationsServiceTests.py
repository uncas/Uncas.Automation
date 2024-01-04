from Services.Google.GooglePresentationsService import readPresentation

def testGooglePresentationsService():
	id = "1AWaGZL1dQOt7TtfslAtxQihv1PB2tsYtKvRkV35_7V0"
	pres = readPresentation(id)
	title = pres["title"]
	text = pres["text"]
	print("The title of the presentation is: " + title)
	print("The text content of the presentation is: " + text)

if __name__ == "__main__":
	testGooglePresentationsService()
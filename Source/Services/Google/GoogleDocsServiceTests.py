from Services.Google.GoogleDocsService import readDocument, read_structural_elements, getListOfTextContent

def test_readDocument():
	# Here's a test docoment that I have used for testing a certain structure:
	# https://docs.google.com/document/d/16dKNw3t1YTIpYiypDDZ-_eYgWbEovSxxyhfzJml98YE/edit
	id = "16dKNw3t1YTIpYiypDDZ-_eYgWbEovSxxyhfzJml98YE"
	doc = readDocument(id)
	title = doc["title"]
	text = doc["text"]
	print("The title of the document is: " + title)
	print("The text content of the document is: " + text)

def test_read_structural_elements():
	import json
	file = "Test/GoogleDocContent.json"
	content = json.load(open(file))
	text = read_structural_elements(content)
	print(text)

def test_getListOfTextContent():
	import json
	file = "Tests/GoogleDocContent.json"
	fileStream = open(file)
	content = json.load(fileStream)
	fileStream.close()
	items = getListOfTextContent(content)
	for item in items:
		print(item)

if __name__ == "__main__":
	test_readDocument()
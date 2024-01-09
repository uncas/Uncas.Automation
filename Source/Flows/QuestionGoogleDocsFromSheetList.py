from Services.Google.GoogleSheetsService import readSheet
from Services.Google.GoogleDocsService import readDocument
from Services.Google.GooglePresentationsService import readPresentation
from Tools.Ai.QaPipeline import questionDocuments
from Utils.FileUtils import writeText

def questionGoogleDocsFromSheetList(sheetId, rangeWithDocLinks, question):
	folder = "Data/GoogleSheetList/" + sheetId
	downloadLinksToFiles(sheetId, rangeWithDocLinks, folder)
	content = questionDocuments(folder, question)

	modelFolder = "../../public/LLMs/dolly-v2-3b/"
	from Tools.Ai.QueryLM import getModel, getTokenizer, generateResponse
	model = getModel(modelFolder)
	tokenizer = getTokenizer(modelFolder)
	relevantContent = "\n".join(map(lambda doc: doc["context"], content))
	prompt = "What is the answer to this question: " + question + "\n\n You can base your answer on the following content:\n\n" + relevantContent
	print(prompt)
	result = generateResponse(prompt, model=model, tokenizer=tokenizer)
	return result

def downloadLinksToFiles(sheetId, rangeWithDocLinks, folder):
	import os
	import re
	rows = readSheet(sheetId, rangeWithDocLinks)
	links = map(lambda row: row[0], rows)
	searches = [
		{
			"regex": 'https://docs.google.com/document/d/(.*)/edit',
			"lookup": readDocument,
			"prefix": "googledoc"
		},
		{
			"regex": 'https://docs.google.com/presentation/d/(.*)/edit',
			"lookup": readPresentation,
			"prefix": "googlepresentation"
		}
	]
	for link in links:
		for search in searches:
			idSearch = re.search(search["regex"], link, re.IGNORECASE)
			if not idSearch:
				continue
			id = idSearch.group(1)
			file = search["prefix"] + "-" + id + ".txt"
			if os.path.exists(folder + "/" + file):
				break
			print("Reading: " + link)
			doc = search["lookup"](id)
			if doc == None:
				print("WARNING: DOCUMENT NOT FOUND OR NOT ACCESSIBLE: " + link)
			else:
				writeText(folder, file, doc["text"])
			break

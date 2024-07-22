from easai.Services.Google.GoogleSheetsService import readSheet
from easai.Services.Google.GoogleDocsService import readDocument
from easai.Services.Google.GooglePresentationsService import readPresentation
from easai.Utils.Settings import getSetting
from easai.Tools.Ai.QaPipeline import questionDocuments
from easai.Utils.FileUtils import write_text

def runQuestionGoogleDocsFromSheetList():
	sheets = getSheetsFromSettings()
	if len(sheets) < 1:
		print("No sheets configured")
		return
	sheet = sheets[0]
	if len(sheets) > 1:
		print("Select sheet:")
		for i in range(len(sheets)):
			print(str(i) + ") " + sheets[i]["sheetId"])
		sheet = sheets[int(input())]
	question = input("Question: ")
	answer = questionGoogleDocsFromSheetList(sheet["sheetId"], sheet["cellRange"], question)
	print("Answer: " + answer)

def getSheetsFromSettings():
	return getSetting("questionGoogleDocsFromSheetList")["sheets"]

def questionGoogleDocsFromSheetList(sheetId, rangeWithDocLinks, question):
	folder = "Data/GoogleSheetList/" + sheetId
	downloadLinksToFiles(sheetId, rangeWithDocLinks, folder)
	content = questionDocuments(folder, question)

	from easai.Tools.Ai.CompletionApis.ChatCompletion import getSingleChatCompletion
	relevantContent = "\n".join(map(lambda doc: doc["context"], content))
	prompt = relevantContent + "\n\n Based on the previous content. What is the answer to this question: " + question
	print(prompt)
	result = getSingleChatCompletion(prompt)
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
				write_text(folder, file, doc["text"])
			break

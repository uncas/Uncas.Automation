from Services.Google.GoogleSheetsService import readSheet
from Services.Google.GoogleDocsService import readDocument
from Tools.Ai.QaPipeline import questionDocuments
from Utils.FileUtils import writeText

def questionGoogleDocsFromSheetList(sheetId, rangeWithDocLinks, question):
	rows = readSheet(sheetId, rangeWithDocLinks)
	links = map(lambda row: row[0], rows)
	docLinks = filter(lambda link: link.startswith("https://docs.google.com/document/"), links)
	folder = "Data/GoogleSheetList/" + sheetId
	# TODO: For completeness, I ought to clean this folder up, or at least remove documents that are no longer active...
	import re
	for docLink in docLinks:
		docIdSearch = re.search('https://docs.google.com/document/d/(.*)/edit', docLink, re.IGNORECASE)
		if docIdSearch:
			docId = docIdSearch.group(1)
			doc = readDocument(docId)
			if doc == None:
				print("WARNING: DOCUMENT NOT FOUND OR NOT ACCESSIBLE: " + docLink)
			else:
				writeText(folder, "googledoc-" + docId + ".txt", doc["text"])
	return questionDocuments(folder, question)

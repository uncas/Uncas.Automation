from Services.Google.GoogleSheetsService import readSheet
from Services.Google.GoogleDocsService import readDocument
from Services.Google.GooglePresentationsService import readPresentation
from Tools.Ai.QaPipeline import questionDocuments
from Utils.FileUtils import writeText

def questionGoogleDocsFromSheetList(sheetId, rangeWithDocLinks, question):
	rows = readSheet(sheetId, rangeWithDocLinks)
	links = map(lambda row: row[0], rows)
	folder = "Data/GoogleSheetList/" + sheetId
	# TODO: For completeness, I ought to clean this folder up, or at least remove documents that are no longer active...
	import re
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
			if idSearch:
				id = idSearch.group(1)
				doc = search["lookup"](id)
				if doc == None:
					print("WARNING: DOCUMENT NOT FOUND OR NOT ACCESSIBLE: " + link)
				else:
					writeText(folder, search["prefix"] + "-" + id + ".txt", doc["text"])
				continue
	return questionDocuments(folder, question)

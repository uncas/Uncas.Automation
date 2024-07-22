def get_resource_tools():
	import re
	from easai.Flows.PersonalAssistant.assistant_tools import AssistantTool, AssistantToolParameter
	resources = getResources()
	idPattern = re.compile("^[a-zA-Z0-9_-]+$")
	for resource in resources:
		id = resource["id"]
		if not idPattern.match(id):
			import logging
			logger = logging.getLogger(__name__)
			logger.fatal("Resource id %s is not valid. Please fix in Settings.json.", id)
			print("Resource id %s is not valid. Please fix in Settings.json:", id)
			exit(1)
		resourceType = resource["resourceType"]
		if resourceType == "OneText":
			yield AssistantTool(
				lambda res = resource: getResourceData(res["id"]), 
				resource["description"], 
				name = "getResourceData_" + id)
		elif resourceType == "DatedEntries":
			yield AssistantTool(
				lambda inputParams = None, res = resource: getDatedEntries(res["id"], inputParams),
				resource["description"],
				[
					AssistantToolParameter("maxNumberOfJournalEntries", "The maximum number of journal entries to return (optional parameter)", type = "integer"),
					AssistantToolParameter("lastNDays", "The number of days to go back (optional parameter)", type = "integer")
				], 
				name = "getDatedEntries_" + id)

def getResources():
	from easai.Utils.Settings import getSetting
	assistant = getSetting("assistant")
	return assistant.get("resources", []) if assistant else []

def getResourceData(resourceId):
	resources = [resource for resource in getResources() if resource["id"] == resourceId]
	if len(resources) == 0:
		return None
	
	resource = resources[0]
	if resource["sourceType"] == "Google Doc" and resource["resourceType"] == "OneText":
		from easai.Services.Google.GoogleDocsService import readDocument
		return readDocument(resource["sourceDetails"]["docId"])
	else:
		return None

def getDatedEntries(resourceId, inputParams = None):
	maxCount = inputParams["maxNumberOfJournalEntries"] if inputParams and "maxNumberOfJournalEntries" in inputParams else None
	lastNDays = inputParams["lastNDays"] if inputParams and "lastNDays" in inputParams else None
	resources = [resource for resource in getResources() if resource["id"] == resourceId]
	if len(resources) == 0:
		return None

	resource = resources[0]
	if resource["sourceType"] == "Google Doc" and resource["resourceType"] == "DatedEntries":
		from easai.Services.Google.GoogleDocsService import getDocumentTexts
		sourceDetails = resource["sourceDetails"]
		texts = getDocumentTexts(sourceDetails["docId"])["texts"]
		entries = mapListOfTextContentToDatedEntries(
			texts, 
			sourceDetails["headingLevel"], 
			sourceDetails["headingText"],
			maxCount,
			lastNDays)
		return entries
	else:
		return None

def mapListOfTextContentToDatedEntries(
		texts : list[str], 
		headingLevel : int, 
		headingText : str, 
		maxCount : int = None, 
		lastNDays : int = None):
	from datetime import datetime, timedelta
	startDate = datetime.now() - timedelta(days = lastNDays + 1) if lastNDays is not None else None
	parentStyle = "HEADING_" + str(headingLevel)
	childStyle = "HEADING_" + str(headingLevel + 1)
	datedEntries = []
	withinParentParagraph = False
	entry = None
	for text in texts:
		if "style" in text and text["style"] == parentStyle and text["text"] == headingText + "\n":
			withinParentParagraph = True
		elif withinParentParagraph and "style" in text and text["style"] == childStyle:
			date = None
			try:
				date = datetime.strptime(text["text"][:10], "%Y-%m-%d")
			except ValueError:
				print("WARNING: Could not parse date, including entry in previous entry:", text["text"][:10])
				continue
			if startDate is not None and date < startDate:
				break
			entry = {"date": {"year":date.year, "month":date.month, "day":date.day}, "texts": []}
			datedEntries.append(entry)
		elif "style" in text and text["style"] == parentStyle and text["text"] != headingText + "\n":
			withinParentParagraph = False
		elif withinParentParagraph:
			entry["texts"].append(text["text"])
	results = [{"date": entry["date"], "text": "".join(entry["texts"])} for entry in datedEntries]
	return results if maxCount is None else results[:maxCount]

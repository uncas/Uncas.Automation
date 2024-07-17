def getResourceTools():
	import re
	from Flows.PersonalAssistant.AssistantTools import AssistantTool
	resources = getResources()
	idPattern = re.compile("^[a-zA-Z0-9_-]+$")
	tools = []
	for resource in resources:
		id = resource["id"]
		if not idPattern.match(id):
			import logging
			logger = logging.getLogger(__name__)
			logger.fatal("Resource id %s is not valid. Please fix in Settings.json.", id)
			print("Resource id %s is not valid. Please fix in Settings.json:", id)
			exit(1)
		#resourceType = resource["type"]
		tool = AssistantTool(lambda x = resource: getResourceData(x["id"]), resource["description"], name = "getResourceData_" + id)
		tools.append(tool)
		#if resourceType == "DatedEntries":
		#	yield AssistantTool(lambda: getDatedEntries(id, maxCount, lastNDays), resource["description"], name = "getDatedEntries_" + id)
	return tools

def getResources():
	from Utils.Settings import getSetting
	return getSetting("assistant")["resources"]

def getResourceData(resourceId):
	resources = [resource for resource in getResources() if resource["id"] == resourceId]
	if len(resources) == 0:
		return None
	
	resource = resources[0]
	if resource["sourceType"] == "Google Doc" and resource["resourceType"] == "OneText":
		from Services.Google.GoogleDocsService import readDocument
		return readDocument(resource["sourceDetails"]["docId"])
	if resource["sourceType"] == "Google Doc" and resource["resourceType"] == "DatedEntries":
		return getDatedEntries(resourceId)
	else:
		return None

def getDatedEntries(resourceId, maxCount = None, lastNDays = None):
	resources = [resource for resource in getResources() if resource["id"] == resourceId]
	if len(resources) == 0:
		return None

	resource = resources[0]
	if resource["sourceType"] == "Google Doc" and resource["resourceType"] == "DatedEntries":
		from Services.Google.GoogleDocsService import getDocumentTexts
		sourceDetails = resource["sourceDetails"]
		texts = getDocumentTexts(sourceDetails["docId"])["texts"]
		return mapListOfTextContentToDatedEntries(texts, sourceDetails["headingLevel"], sourceDetails["headingText"])
	else:
		return None

def mapListOfTextContentToDatedEntries(texts : list[str], headingLevel : int, headingText : str):
	import datetime
	parentStyle = "HEADING_" + str(headingLevel)
	childStyle = "HEADING_" + str(headingLevel + 1)
	datedEntries = []
	withinParentParagraph = False
	entry = None
	for text in texts:
		if "style" in text and text["style"] == parentStyle and text["text"] == headingText + "\n":
			withinParentParagraph = True
		elif withinParentParagraph and "style" in text and text["style"] == childStyle:
			date = datetime.datetime.strptime(text["text"][:10], "%Y-%m-%d")
			entry = {"date": {"year":date.year, "month":date.month, "day":date.day}, "texts": []}
			datedEntries.append(entry)
		elif "style" in text and text["style"] == parentStyle and text["text"] != headingText + "\n":
			withinParentParagraph = False
		elif withinParentParagraph:
			entry["texts"].append(text["text"])
	return [{"date": entry["date"], "text": "".join(entry["texts"])} for entry in datedEntries]

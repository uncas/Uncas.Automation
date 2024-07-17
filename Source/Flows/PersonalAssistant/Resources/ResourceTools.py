def getResourceTools():
	import re
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
		yield {
			"method": lambda: getResourceData(id),
			"name": "getResourceData_" + id,
			"description": resource["description"],
			"parameters": {}
		}

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
	else:
		return None

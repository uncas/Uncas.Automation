def getLocation():
	import requests
	url = "https://ipapi.co/json/"
	r = requests.get(url)
	data = r.json()
	return {
		"city": data["city"],
		"state": data["region"],
		"country": data["country_name"]
	}

def getLocationTool():
	from Flows.PersonalAssistant.AssistantTools import AssistantTool
	return AssistantTool(getLocation, "Get the user's current location")
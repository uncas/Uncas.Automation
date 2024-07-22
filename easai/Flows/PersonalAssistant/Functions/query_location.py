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

def get_location_tool():
	from easai.Flows.PersonalAssistant.assistant_tools import AssistantTool
	return AssistantTool(getLocation, "Get the user's current location")
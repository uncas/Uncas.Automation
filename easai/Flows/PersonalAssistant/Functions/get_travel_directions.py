def getTravelDirections(data):
	fromLocation = data["fromLocation"]
	toLocation = data["toLocation"]
	from Services.Google.GoogleMapsService import GoogleMapsService
	return GoogleMapsService.GetDirections(fromLocation, toLocation)

def get_travel_directions_tool():
	from Flows.PersonalAssistant.assistant_tools import AssistantTool, AssistantToolParameter
	return AssistantTool(getTravelDirections, "Get travel directions", [
		AssistantToolParameter("fromLocation", "The location to start from"),
		AssistantToolParameter("toLocation", "The location to go to")
	])
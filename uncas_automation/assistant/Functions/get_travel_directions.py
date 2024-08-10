def getTravelDirections(fromLocation, toLocation):
	from uncas_automation.Services.Google.GoogleMapsService import GoogleMapsService
	return GoogleMapsService.GetDirections(fromLocation, toLocation)

def get_travel_directions_tool():
	from easai.assistant.tool import AssistantTool, AssistantToolParameter
	return AssistantTool(getTravelDirections, "Get travel directions", [
		AssistantToolParameter("fromLocation", "The location to start from"),
		AssistantToolParameter("toLocation", "The location to go to")
	])
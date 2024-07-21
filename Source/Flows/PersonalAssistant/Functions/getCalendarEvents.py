def getCalendarEvents():
	from Services.Google.GoogleCalendarService import getCalendarEvents
	return list(getCalendarEvents(20))

def getTodaysCalendarEvents():
	from Services.Google.GoogleCalendarService import getTodaysCalendarEvents
	return list(getTodaysCalendarEvents(20))

def getTodaysCalendarEventsTool():
	from Flows.PersonalAssistant.AssistantTools import AssistantTool
	return AssistantTool(getTodaysCalendarEvents, "Get todays calendar events")
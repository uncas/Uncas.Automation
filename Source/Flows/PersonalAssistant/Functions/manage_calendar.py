def getCalendarEvents():
	from Services.Google.GoogleCalendarService import getCalendarEvents
	return list(getCalendarEvents(20))

def get_todays_calendar_events():
	from Services.Google.GoogleCalendarService import getTodaysCalendarEvents
	return list(getTodaysCalendarEvents(20))

def get_todays_calendar_events_tool():
	from Flows.PersonalAssistant.assistant_tools import AssistantTool
	return AssistantTool(get_todays_calendar_events, "Get todays calendar events")
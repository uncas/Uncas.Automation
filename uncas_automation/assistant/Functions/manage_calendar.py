def getCalendarEvents():
	from uncas_automation.Services.Google.GoogleCalendarService import getCalendarEvents
	return list(getCalendarEvents(20))

def get_todays_calendar_events():
	from uncas_automation.Services.Google.GoogleCalendarService import getTodaysCalendarEvents
	return list(getTodaysCalendarEvents(20))

def get_todays_calendar_events_tool():
	from easai.assistant.tool import AssistantTool
	return AssistantTool(get_todays_calendar_events, "Get todays calendar events")
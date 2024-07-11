def getCalendarEvents():
	from Services.Google.GoogleCalendarService import getCalendarEvents
	return list(getCalendarEvents(10))
def getCalendarEvents():
	from Services.Google.GoogleCalendarService import getCalendarEvents
	return list(getCalendarEvents(20))

def getTodaysCalendarEvents():
	from Services.Google.GoogleCalendarService import getTodaysCalendarEvents
	return list(getTodaysCalendarEvents(20))
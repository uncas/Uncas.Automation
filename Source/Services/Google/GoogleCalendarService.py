# From: https://developers.google.com/calendar/api/quickstart/python

import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from Services.Google.GoogleAuth import getCredentials

def getCalendarEvents(maxResults, timeMin = None):
	creds = getCredentials()
	try:
		service = build("calendar", "v3", credentials=creds)
		if not timeMin:
			timeMin = datetime.datetime.utcnow().isoformat() + "Z"
		events_result = (
			service.events().list(
				calendarId = "primary",
				timeMin = timeMin,
				maxResults = maxResults,
				singleEvents = True,
				orderBy = "startTime",
			).execute())
		events = events_result.get("items", [])
		for event in events:
			start = event["start"].get("dateTime", event["start"].get("date"))
			yield {
				"title": event["summary"],
				"start": start
			}
	except HttpError as err:
		print(err)

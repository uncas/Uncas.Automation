# From: https://developers.google.com/calendar/api/quickstart/python

import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from Services.Google.GoogleAuth import getCredentials

def getTodaysCalendarEvents(maxResults = 20):
	fromDaysInFuture = 0
	now = datetime.datetime.utcnow()
	midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
	oneMinuteBeforeNextMidnight = midnight + datetime.timedelta(days=1) - datetime.timedelta(seconds = 1)
	toDaysInFuture = (oneMinuteBeforeNextMidnight - now).seconds / (60 * 60 * 24)
	return getCalendarEvents(maxResults, fromDaysInFuture, toDaysInFuture)

def getCalendarEvents(maxResults = 20, fromDaysInFuture = 0, toDaysInFuture = 1):
	import json
	from Utils.FileUtils import write_text
	creds = getCredentials()
	try:
		service = build("calendar", "v3", credentials=creds)
		timeMin = (datetime.datetime.utcnow() + datetime.timedelta(days = fromDaysInFuture)).isoformat() + "Z"
		timeMax = (datetime.datetime.utcnow() + datetime.timedelta(days = toDaysInFuture)).isoformat() + "Z"
		events_result = (
			service.events().list(
				calendarId = "primary",
				timeMin = timeMin,
				timeMax = timeMax,
				maxResults = maxResults,
				singleEvents = True,
				orderBy = "startTime",
			).execute())
		events = events_result.get("items", [])
		for event in events:
			write_text("Data/Calendar", event["id"] + ".json", json.dumps(event, indent = 4))
			start = event["start"].get("dateTime", event["start"].get("date"))
			status = getEventStatus(event)
			if status == "declined":
				continue
			yield {
				"id": event["id"],
				"title": event["summary"],
				"start": start,
				"status": status,
				"eventType": event["eventType"],
				"description": event["description"] if "description" in event else None
			}
	except HttpError as err:
		print(err)

def getEventStatus(event):
	selfAttendees = [attendee for attendee in event["attendees"] if "self" in attendee and attendee["self"]] if "attendees" in event else []
	return selfAttendees[0]["responseStatus"] if len(selfAttendees) > 0 else event["status"]

def test_getCalendarEvents():
	for item in getTodaysCalendarEvents(10):
		print(item)
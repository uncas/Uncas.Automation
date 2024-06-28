# From: https://developers.google.com/calendar/api/quickstart/python

def readNextEvents(count):
  from googleapiclient.discovery import build
  from googleapiclient.errors import HttpError
  from GoogleAuth import getCredentials
  import datetime

  creds = getCredentials()
  try:
    service = build("calendar", "v3", credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
      service.events()
        .list(calendarId="primary", timeMin=now, maxResults=count, singleEvents=True, orderBy="startTime")
        .execute()
    )
    events = events_result.get("items", [])
    if not events:
      return []
    return events
  except HttpError as err:
    print(err)
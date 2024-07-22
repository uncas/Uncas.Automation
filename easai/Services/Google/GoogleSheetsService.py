# From: https://developers.google.com/sheets/api/quickstart/python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from Services.Google.GoogleAuth import getCredentials

def readSheet(id, range):
	creds = getCredentials()
	try:
		service = build("sheets", "v4", credentials = creds)
		sheet = service.spreadsheets()
		result = (sheet.values().get(spreadsheetId = id, range = range).execute())
		values = result.get("values", [])
		if not values:
			print("No data found.")
			return
		return values
	except HttpError as err:
		print(err)

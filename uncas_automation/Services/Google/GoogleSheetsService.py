# From: https://developers.google.com/sheets/api/quickstart/python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from uncas_automation.Services.Google.GoogleAuth import getCredentials

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

def replace_data_in_sheet(account, document_id, sheet_name, data):
	creds = getCredentials(account)
	try:
		service = build("sheets", "v4", credentials = creds)
		clear_sheet(service, document_id, sheet_name)
		sheet = service.spreadsheets()
		range = sheet_name + "!A1"
		sheet.values().update(spreadsheetId = document_id, range = range, valueInputOption = "USER_ENTERED", body = {"values": data}).execute()
	except HttpError as err:
		print(err)

def clear_sheet(service, document_id, sheet_name):
	service.spreadsheets().values().clear(
    	spreadsheetId=document_id,
    	range=sheet_name + "!A1:AZ"
	).execute()
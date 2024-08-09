from uncas_automation.Services.Google.GoogleSheetsService import readSheet

def testGoogleSheetsService():
	id = "xx"
	range = "Ark1!A:D"
	values = readSheet(id, range)
	for row in values:
		print(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}")

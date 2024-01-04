from GoogleSheetsService import readSheet

id = "1X9QhUocllUsrhW07g2X2O3CqBuURAFMXBqmjqkePvN8"
range = "Ark1!A:D"
values = readSheet(id, range)
for row in values:
	print(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}")

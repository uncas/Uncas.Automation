def getDateAndTime():
	import datetime
	return {
		"date": datetime.date.today().strftime("%Y-%m-%d"),
		"time": datetime.datetime.now().strftime("%H:%M:%S")
	}
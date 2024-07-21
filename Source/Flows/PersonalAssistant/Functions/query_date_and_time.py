def getDateAndTime():
	import datetime
	return {
		"date": datetime.date.today().strftime("%Y-%m-%d"),
		"time": datetime.datetime.now().strftime("%H:%M:%S")
	}

def get_date_and_time_tool():
	from Flows.PersonalAssistant.AssistantTools import AssistantTool
	return AssistantTool(getDateAndTime, "Get current date and time")
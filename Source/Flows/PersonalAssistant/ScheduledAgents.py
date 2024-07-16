def runScheduledAgents():
	import datetime
	from Utils.FileUtils import appendText
	from Flows.PersonalAssistant.Agents.MailCalendarTaskAgent import MailCalendarTaskAgent
	from Flows.PersonalAssistant.PersonalAssistant import runTaskedAgent

	appendText("Data", "LastRun.txt", "\nLast run started at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	runTaskedAgent(MailCalendarTaskAgent())
	appendText("Data", "LastRun.txt", "\nLast run completed at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

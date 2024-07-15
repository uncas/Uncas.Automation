def runScheduledAgents():
	import datetime
	from Utils.FileUtils import appendText
	appendText("Data", "LastRun.txt", "\nLast run at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

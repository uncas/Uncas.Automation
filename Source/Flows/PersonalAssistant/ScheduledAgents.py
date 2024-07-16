def runScheduledAgents():
	from Flows.PersonalAssistant.Agents.MailCalendarTaskAgent import MailCalendarTaskAgent
	from Flows.PersonalAssistant.PersonalAssistant import runTaskedAgent
	import logging
	from Flows.PersonalAssistant.LoggerSetup import initLogger
	initLogger()
	logger = logging.getLogger(__name__)
	logger.info("Starting scheduled agents")
	runTaskedAgent(MailCalendarTaskAgent())
	logger.info("Completed scheduled agents")

def runScheduledAgents():
	from easai.Flows.PersonalAssistant.Agents.mail_calendar_task_agent import MailCalendarTaskAgent
	from easai.Flows.PersonalAssistant.personal_assistant import runTaskedAgent
	import logging
	from easai.Flows.PersonalAssistant.logger_setup import initLogger
	initLogger()
	logger = logging.getLogger(__name__)
	logger.info("Starting scheduled agents")
	#runTaskedAgent(MailCalendarTaskAgent())
	logger.info("Completed scheduled agents")

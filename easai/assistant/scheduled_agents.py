def runScheduledAgents():
	from easai.assistant.Agents.mail_calendar_task_agent import MailCalendarTaskAgent
	from easai.assistant.personal_assistant import run_tasked_agent
	import logging
	from easai.assistant.logger_setup import init_logger
	init_logger()
	logger = logging.getLogger(__name__)
	logger.info("Starting scheduled agents")
	#runTaskedAgent(MailCalendarTaskAgent())
	logger.info("Completed scheduled agents")

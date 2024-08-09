import logging

from uncas_automation.assistant.logger_setup import init_logger
from uncas_automation.assistant.personal_assistant import run_tasked_agent
from uncas_automation.assistant.Agents.mail_calendar_task_agent import MailCalendarTaskAgent

def run_scheduled_agents():
	init_logger()
	logger = logging.getLogger(__name__)
	logger.info("Starting scheduled agents")
	#run_tasked_agent(MailCalendarTaskAgent())
	logger.info("Completed scheduled agents")

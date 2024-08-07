import logging

from easai.assistant.logger_setup import init_logger
from easai.assistant.personal_assistant import run_tasked_agent
from easai.assistant.Agents.mail_calendar_task_agent import MailCalendarTaskAgent

def run_scheduled_agents():
	init_logger()
	logger = logging.getLogger(__name__)
	logger.info("Starting scheduled agents")
	#run_tasked_agent(MailCalendarTaskAgent())
	logger.info("Completed scheduled agents")

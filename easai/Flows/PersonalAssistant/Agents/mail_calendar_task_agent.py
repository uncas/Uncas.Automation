from easai.Flows.PersonalAssistant.Agents.agent_definition import AgentDefinition

class MailCalendarTaskAgent(AgentDefinition):
	# Read mail, calendar, tasks
	# Ask AI to summarize and suggest actions (via good system prompt)
	# The AI should have access to certain tools in case it wants to lookup further information
	# The summary gets posted as a jira task for me to read!

	def __init__(self):
		import datetime
		from easai.Flows.PersonalAssistant.Functions.manage_calendar import get_todays_calendar_events
		from easai.Flows.PersonalAssistant.Functions.manage_jira import get_my_jira_issues, create_jira_issue
		from easai.Flows.PersonalAssistant.Functions.read_email import read_email
		from easai.Flows.PersonalAssistant.assistant_tools import get_all_tools

		system_prompt_file = "TaskCalendarMailAssistant.md"
		system_prompt = AgentDefinition.get_system_prompt_from_file(system_prompt_file)

		input_tasks = []
		input_tasks.append({ "task": lambda: get_todays_calendar_events(), "prompt": "Today's calendar events" })
		input_tasks.append({ "task": lambda: get_my_jira_issues(), "prompt": "My jira issues" })
		input_tasks.append({ "task": lambda: read_email(), "prompt": "My mails" })

		task_summary = "Task/Calendar/Mail assistant summary, " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
		action_on_result = lambda result : create_jira_issue({"summary": task_summary, "description": result})
		super().__init__(system_prompt, input_tasks, action_on_result, tools = get_all_tools())

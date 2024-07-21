from Flows.PersonalAssistant.Agents.agent_definition import AgentDefinition

class MailCalendarTaskAgent(AgentDefinition):
	# Read mail, calendar, tasks
	# Ask AI to summarize and suggest actions (via good system prompt)
	# The AI should have access to certain tools in case it wants to lookup further information
	# The summary gets posted as a jira task for me to read!

	def __init__(self):
		import datetime
		from Flows.PersonalAssistant.Functions.manage_calendar import getTodaysCalendarEvents
		from Flows.PersonalAssistant.Functions.manage_jira import getMyJiraIssues, createJiraIssue
		from Flows.PersonalAssistant.Functions.read_email import readEmail
		from Flows.PersonalAssistant.AssistantTools import get_all_tools

		systemPromptFile = "TaskCalendarMailAssistant.md"
		systemPrompt = AgentDefinition.get_system_prompt_from_file(systemPromptFile)

		inputTasks = []
		inputTasks.append({ "task": lambda: getTodaysCalendarEvents(), "prompt": "Today's calendar events" })
		inputTasks.append({ "task": lambda: getMyJiraIssues(), "prompt": "My jira issues" })
		inputTasks.append({ "task": lambda: readEmail(), "prompt": "My mails" })

		taskSummary = "Task/Calendar/Mail assistant summary, " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
		actionOnResult = lambda result : createJiraIssue({"summary": taskSummary, "description": result})
		super().__init__(systemPrompt, inputTasks, actionOnResult, tools = get_all_tools())

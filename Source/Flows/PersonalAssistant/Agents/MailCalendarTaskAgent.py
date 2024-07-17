from Flows.PersonalAssistant.Agents.AgentDefinition import AgentDefinition

class MailCalendarTaskAgent(AgentDefinition):
	# Read mail, calendar, tasks
	# Ask AI to summarize and suggest actions (via good system prompt)
	# The AI should have access to certain tools in case it wants to lookup further information
	# The summary gets posted as a jira task for me to read!

	def __init__(self):
		import datetime
		from Flows.PersonalAssistant.Functions.getCalendarEvents import getTodaysCalendarEvents
		from Flows.PersonalAssistant.Functions.createJiraIssue import getMyJiraIssues, createJiraIssue
		from Flows.PersonalAssistant.Functions.readEmail import readEmail

		systemPromptFile = "TaskCalendarMailAssistant.md"

		inputTasks = []
		inputTasks.append({ "task": lambda: getTodaysCalendarEvents(), "prompt": "Today's calendar events" })
		inputTasks.append({ "task": lambda: getMyJiraIssues(), "prompt": "My jira issues" })
		inputTasks.append({ "task": lambda: readEmail(), "prompt": "My mails" })

		taskSummary = "Task/Calendar/Mail assistant summary, " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
		actionOnResult = lambda result : createJiraIssue({"summary": taskSummary, "description": result})

		super().__init__(systemPromptFile, inputTasks, actionOnResult)

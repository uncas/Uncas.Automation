# The module: https://pypi.org/project/jira/
# Documentation of module: https://jira.readthedocs.io/examples.html
# API KEYS: https://id.atlassian.com/manage-profile/security/api-tokens

import os

def initJira():
	from jira import JIRA
	jiraUser = os.getenv("ATLASSIAN_USER") # The email address used on your Jira account, check here if in doubt: https://id.atlassian.com/manage-profile/profile-and-visibility
	apiToken = os.getenv("ATLASSIAN_API_TOKEN") # Token created here: https://id.atlassian.com/manage-profile/security/api-tokens
	jiraServer = os.getenv("JIRA_SERVER") # The base URL of your Jira installation, for example if a link to an issue is https://example-jira.atlassian.net/browse/MYPROJ-123, then Jira server is https://example-jira.atlassian.net
	return JIRA(jiraServer, basic_auth=(jiraUser, apiToken))

def getMyJiraIssues():
	jira = initJira()
	jql = os.getenv("JIRA_JQL_MY_ISSUES")
	if not jql:
		jql = "assignee = currentUser() AND Resolution = unresolved"
	issues = jira.search_issues(jql, fields='summary,description,due')
	#for issue in issues:
	#	for field_name in issue.raw['fields']:
	#		print("Field:", field_name, "Value:", issue.raw['fields'][field_name])
	return [{
		"key": issue.key,
		"summary": getFieldValue(issue, "summary"),
		"description": getFieldValue(issue, "description"),
		"due": getFieldValue(issue, "due")
	} for issue in issues]

def getFieldValue(issue, fieldName):
	return issue.raw['fields'][fieldName]

def createJiraIssue(data):
	summary = data["summary"]
	description = data["description"]
	jira = initJira()
	jiraProject = os.getenv("JIRA_PROJECT")
	issue = jira.create_issue(
		project = jiraProject,
		summary = summary,
		description = description,
		issuetype = {'name': 'Task'})
	return {"key": issue.key, "summary": issue.fields.summary, "description": issue.fields.description}

def createJiraIssueTool():
	from Flows.PersonalAssistant.AssistantTools import AssistantTool, AssistantToolParameter
	return AssistantTool(createJiraIssue, "Create a Jira issue", [
		AssistantToolParameter("summary", "The summary of the issue"),
		AssistantToolParameter("description", "The description of the issue")
	])

def getMyJiraIssuesTool():
	from Flows.PersonalAssistant.AssistantTools import AssistantTool
	return AssistantTool(getMyJiraIssues, "Get all my Jira issues")
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
	jql = "assignee = currentUser() AND Resolution = unresolved"
	return jira.search_issues(jql, fields='summary,description')

def createJiraIssue(data):
	summary = data["summary"]
	description = data["description"]
	jira = initJira()
	jiraProject = os.getenv("JIRA_PROJECT")
	return jira.create_issue(
		project = jiraProject,
		summary = summary,
		description = description,
		issuetype = {'name': 'Task'})
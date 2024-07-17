class AssistantTool:
	def __init__(self, method, description, parameters = [], name = None):
		self.parameters = parameters
		self.description = description
		self.method = method
		self.name = name if name else method.__name__
	
	def mapToOpenAiTool(self):
		properties = {}
		for parameter in self.parameters:
			properties[parameter.name] = parameter.getOpenAiToolProperties()
		return {
			"type": "function",
			"function": {
				"name": self.name,
				"description": self.description,
				"parameters": {
					"type": "object",
					"properties": properties
				}
			}
		}

class AssistantToolParameter:
	def __init__(self, name, description, type = "string", enum = None):
		self.name = name
		self.description = description
		self.type = type
		self.enum = enum
	
	def getOpenAiToolProperties(self):
		value = {
			"type": self.type,
			"description": self.description
		}
		if self.enum:
			value["enum"] = self.enum
		return value

def getTools():
	from Flows.PersonalAssistant.Functions.getLocation import getLocation
	from Flows.PersonalAssistant.Functions.getCurrentWeather import getCurrentWeather
	from Flows.PersonalAssistant.Functions.theMovieDb import getWatchProviders, getUnwatchedGoodWatchableMovies
	from Flows.PersonalAssistant.Functions.findInfoInDocs import findInfoInDocs
	from Flows.PersonalAssistant.Functions.getLatestNews import getLatestNews
	from Flows.PersonalAssistant.Functions.getLatestNews import getNewsDetails
	from Flows.PersonalAssistant.Functions.searchArxiv import searchArxiv
	from Flows.PersonalAssistant.Functions.readEmail import readEmail
	from Flows.PersonalAssistant.Functions.readEmail import writeEmail
	from Flows.PersonalAssistant.Functions.createJiraIssue import createJiraIssue
	from Flows.PersonalAssistant.Functions.createJiraIssue import getMyJiraIssues
	from Flows.PersonalAssistant.Functions.getCalendarEvents import getTodaysCalendarEvents
	from Flows.PersonalAssistant.Functions.getDateAndTime import getDateAndTime
	from Flows.PersonalAssistant.Functions.readWebPage import readWebPage
	from Flows.PersonalAssistant.Resources.ResourceTools import getResourceTools

	tools = [
		AssistantTool(getLocation, "Get the user's current location"),
		AssistantTool(getCurrentWeather, "Gets the current weather", [
			AssistantToolParameter("countryCode", "The country code of the country where to get the weather"),
			AssistantToolParameter("city", "The city from where to get the weather")
		]),
		AssistantTool(getWatchProviders, "Gets watch providers for a given movie", [
			AssistantToolParameter("movieTitle", "The title of the movie")
		]),
		AssistantTool(findInfoInDocs, "Find info in work-related documentation", [
			AssistantToolParameter("query", "The thing to search for in the documentation")
		]),
		AssistantTool(getUnwatchedGoodWatchableMovies, "Get unwatched good watchable movies"),
		AssistantTool(getLatestNews, "Get the latest news"),
		AssistantTool(getNewsDetails, "Get details about news in the provided link", [
			AssistantToolParameter("newsLink", "The link to the news")
		]),
		AssistantTool(searchArxiv, "Search arXiv.org for articles on physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, electrical engineering and systems science, and economics", [
			AssistantToolParameter("query", "The query to search for"),
			AssistantToolParameter("maxResults", "The maximum number of results to return", type = "integer"),
			AssistantToolParameter("sortBy", "The field to sort by", enum = ["relevance", "lastUpdatedDate", "submittedDate"]),
			AssistantToolParameter("sortOrder", "The order to sort by", enum = ["ascending", "descending"])
		]),
		AssistantTool(readEmail, "Read email"),
		AssistantTool(writeEmail, "Write an email", [
			AssistantToolParameter("recipient", "The recipient of the email"),
			AssistantToolParameter("subject", "The subject of the email"),
			AssistantToolParameter("body", "The body of the email"),
			AssistantToolParameter("internalMessageId", "The internal id of the message that should be replied to (used only when replying to an email)")
		]),
		AssistantTool(createJiraIssue, "Create a task for me as a Jira issue", [
			AssistantToolParameter("summary", "A short summary of the issue"),
			AssistantToolParameter("description", "A detailed description of the issue")
		]),
		AssistantTool(getMyJiraIssues, "Get my issues from Jira"),
		AssistantTool(getTodaysCalendarEvents, "Get todays calendar events"),
		AssistantTool(getDateAndTime, "Get current date and time"),
		AssistantTool(readWebPage, "Read web page", [
			AssistantToolParameter("url", "The URL of the web page to read")
		]),
		AssistantTool(getUnwatchedGoodWatchableMovies, "Get unwatched good watchable movies")
	]

	for tool in getResourceTools():
		tools.append(tool)
	
	return tools
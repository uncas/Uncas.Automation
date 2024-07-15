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

	return [
		{
			"method": getCurrentWeather,
			"description": "Gets the current weather",
			"parameters": {
				"countryCode": {
					"type": "string",
					"description": "The country code from where to get the weather"
				},
				"city": {
					"type": "string",
					"description": "The city from where to get the weather"
				}
			}
		},
		{
			"method": getLocation,
			"description": "Get the user's current location",
			"parameters": {}
		},
		{
			"method": getWatchProviders,
			"description": "Gets watch providers for a given movie",
			"parameters": {
				"movieTitle": {
					"type": "string",
					"description": "The title of the movie"
				}
			}
		},
		{
			"method": findInfoInDocs,
			"description": "Find info in work-related documentation",
			"parameters": {
				"query": {
					"type": "string",
					"description": "The thing to search for in the documentation"
				}
			}
		},
		{
			"method": getLatestNews,
			"description": "Get the latest news",
			"parameters": {}
		},
		{
			"method": getNewsDetails,
			"description": "Get details about news in the provided link.",
			"parameters": {
				"newsLink": {
					"type": "string",
					"description": "The link to the news"
				}
			}
		},
		{
			"method": searchArxiv,
			"description": "Search arXiv.org for articles on physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, electrical engineering and systems science, and economics",
			"parameters": {
				"query": {
					"type": "string",
					"description": "The query to search for"
				},
				"maxResults": {
					"type": "integer",
					"description": "The maximum number of results to return"
				},
				"sortBy": {
					"type": "string",
					"description": "The field to sort by",
					"enum": ["relevance", "lastUpdatedDate", "submittedDate"]
				},
				"sortOrder": {
					"type": "string",
					"description": "The order to sort by",
					"enum": ["ascending", "descending"]
				}
			}
		},
		{
			"method": readEmail,
			"description": "Read email",
			"parameters": {}
		},
		{
			"method": writeEmail,
			"description": "Write an email",
			"parameters": {
				"recipient": {
					"type": "string",
					"description": "The recipient of the email"
				},
				"subject": {
					"type": "string",
					"description": "The subject of the email"
				},
				"body": {
					"type": "string",
					"description": "The body of the email"
				},
				"internalMessageId": {
					"type": "string",
					"description": "The internal id of the message that should be replied to (used only when replying to an email)"
				}
			}
		},
		{
			"method": createJiraIssue,
			"description": "Create a task for me as a Jira issue",
			"parameters": {
				"summary": {
					"type": "string",
					"description": "A short summary of the issue"
				},
				"description": {
					"type": "string",
					"description": "A detailed description of the issue"
				}
			}
		},
		{
			"method": getMyJiraIssues,
			"description": "Get my issues from Jira",
			"parameters": {}
		},
		{
			"method": getTodaysCalendarEvents,
			"description": "Get today's events from the user's calendar",
			"parameters": {}
		},
		{
			"method": getDateAndTime,
			"description": "Get current date and time",
			"parameters": {}
		},
		{
			"method": readWebPage,
			"description": "Read web page",
			"parameters": {
				"url": {
					"type": "string",
					"description": "The URL of the web page to read"
				}
			}
		},
		{
			"method": getUnwatchedGoodWatchableMovies,
			"description": "Get unwatched good watchable movies",
			"parameters": {}
		}
	]
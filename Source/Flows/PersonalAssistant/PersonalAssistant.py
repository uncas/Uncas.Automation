from dotenv import load_dotenv

load_dotenv(override = True)

def getTools():
	from Flows.PersonalAssistant.Functions.getLocation import getLocation
	from Flows.PersonalAssistant.Functions.getCurrentWeather import getCurrentWeather
	from Flows.PersonalAssistant.Functions.theMovieDb import getWatchProviders
	from Flows.PersonalAssistant.Functions.findInfoInDocs import findInfoInDocs
	from Flows.PersonalAssistant.Functions.getLatestNews import getLatestNews
	from Flows.PersonalAssistant.Functions.getLatestNews import getNewsDetails
	from Flows.PersonalAssistant.Functions.searchArxiv import searchArxiv
	from Flows.PersonalAssistant.Functions.readEmail import readEmail
	from Flows.PersonalAssistant.Functions.readEmail import writeEmail

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
				"sender": {
					"type": "string",
					"description": "The sender of the email"
				},
				"internalMessageId": {
					"type": "string",
					"description": "The internal id of the message that should be replied to (used only when replying to an email)"
				}
			}
		}
	]

def chat_with_chatgpt(prompt, model="gpt-3.5-turbo"):
	import json
	from openai import OpenAI

	maxIterations = 3

	toolList = getTools()
	tools = [
		{
			"type": "function",
			"function": {
				"name": tool["method"].__name__,
				"description": tool["description"],
				"parameters": {
					"type": "object",
					"properties": tool["parameters"]
				}
			}
		} for tool in toolList
	]
	toolMethods = {tool["method"].__name__: tool["method"] for tool in toolList}
	client = OpenAI()
	messages = [{
			"role": "user",
			"content": prompt,
	}]
	for _ in range(maxIterations):
		chat_completion = client.chat.completions.create(
			messages = messages,
			model = model,
			tools = tools
		)
		choice = chat_completion.choices[0]
		finishReason = choice.finish_reason
		message = choice.message
		if finishReason == "stop":
			return message.content
		elif finishReason == "tool_calls":
			messages.append(message)
			for toolCall in message.tool_calls:
				callFunction = toolCall.function
				if callFunction.name in toolMethods:
					functionName = callFunction.name
					functionArgs = json.loads(callFunction.arguments)
					functionResponse = None
					toolMethod = toolMethods[functionName]
					if functionArgs:
						print("Calling function: ", functionName, " with args: ", functionArgs)
						functionResponse = toolMethod(functionArgs)
					else:
						print("Calling function: ", functionName, " without args.")
						functionResponse = toolMethod()
					messages.append({
						"role": "tool",
						"name": functionName,
						"tool_call_id": toolCall.id,
						"content": json.dumps(functionResponse)
					})


def testIt():
	#from Flows.PersonalAssistant.Functions.findInfoInDocs import syncDocs # type: ignore
	#syncDocs()

	#from Flows.PersonalAssistant.Functions.findInfoInDocs import findInfoInDocs # type: ignore
	#info = findInfoInDocs("What are the plans for the office space?")
	#print(info)

	#from Flows.PersonalAssistant.Functions.getLatestNews import getNewsDetails, getLatestNews
	#news = getLatestNews()
	#print(news)
	#print(getNewsDetails(news[0]))

	#from Flows.PersonalAssistant.Functions.searchArxiv import searchArxiv
	#papers = searchArxiv({"query": "rag"})
	#print(papers)

	#from Flows.PersonalAssistant.Functions.getCurrentWeather import getCurrentWeather
	#weather = getCurrentWeather({"city": "Odder", "countryCode": "DK"})
	#print("Weather: ", weather)

	#from Flows.PersonalAssistant.Functions.theMovieDb import getRecommendedMoviesThatIHaveAccessToWatch
	#movies = getRecommendedMoviesThatIHaveAccessToWatch()
	#for movie in movies:
	#	print(movie["rating"], movie["title"], movie["providers"])

	#from Services.TheMovieDb.TmdbService import TmdbService
	#tmdbService = TmdbService()
	#tmdbService.rateMovieByTitle("Ashes of Time", 10)
	#tmdbService.rateMovieByTitle("The Godfather", 9)
	#print(tmdbService.getMyFavoriteMovies())
	#print(tmdbService.getMoviesIHaveWatched())

	#from Flows.PersonalAssistant.Functions.generateImage import generateImage, makePartOfImageTransparent
	#image = generateImage("A steampunk city with gear-driven machines, airships docked atop buildings, and streets lit by gas lamps, set in a vast canyon")
	#print(image)

	#from pathlib import Path
	#downloadsPath = str(Path.home() / "Downloads")
	#originalFilePath = downloadsPath + "/skriget.jpg"
	#newFilePath = downloadsPath + "/skriget_transparent.png"
	#xFraction, yFraction, widthFraction, heightFraction = 0.1, 0.1, 0.5, 0.5
	#makePartOfImageTransparent(originalFilePath, newFilePath, xFraction, yFraction, widthFraction, heightFraction)

	from Flows.PersonalAssistant.Functions.createAssistant import createAndRunAssistant
	createAndRunAssistant()

def runIt():
	prompt = input("Prompt : ")
	response = chat_with_chatgpt(prompt)
	print("Response: ", response)

def runPersonalAssistant():
	#testIt()
	runIt()

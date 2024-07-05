from dotenv import load_dotenv

load_dotenv()

def getTools():
	from Flows.PersonalAssistant.Functions.getLocation import getLocation
	from Flows.PersonalAssistant.Functions.getCurrentWeather import getCurrentWeather
	from Flows.PersonalAssistant.Functions.theMovieDb import getWatchProviders
	from Flows.PersonalAssistant.Functions.findInfoInDocs import findInfoInDocs
	from Flows.PersonalAssistant.Functions.getLatestNews import getLatestNews
	from Flows.PersonalAssistant.Functions.getLatestNews import getNewsDetails
	from Flows.PersonalAssistant.Functions.searchArxiv import searchArxiv

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

	from Flows.PersonalAssistant.Functions.getCurrentWeather import getCurrentWeather
	weather = getCurrentWeather({"city": "Odder", "countryCode": "DK"})
	print("Weather: ", weather)

def runIt():
	prompt = input("Prompt : ")
	response = chat_with_chatgpt(prompt)
	print("Response: ", response)

def runPersonalAssistant():
	#testIt()
	runIt()

from dotenv import load_dotenv

load_dotenv()

def getTools():
	from Flows.PersonalAssistant.Functions.getLocation import getLocation
	from Flows.PersonalAssistant.Functions.getCurrentWeather import getCurrentWeather
	from Flows.PersonalAssistant.Functions.theMovieDb import getWatchProviders
	from Flows.PersonalAssistant.Functions.findInfoInDocs import findInfoInDocs
	return [
		{
			"method": getCurrentWeather,
			"description": "Gets the current weather",
			"parameters": {
				"country": {
					"type": "string",
					"description": "The country from where to get the weather"
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


def testingIt():
	#from Flows.PersonalAssistant.Functions.findInfoInDocs import syncDocs # type: ignore
	#syncDocs()

	from Flows.PersonalAssistant.Functions.findInfoInDocs import findInfoInDocs # type: ignore
	info = findInfoInDocs("What are the plans for the office space?")
	print(info)

def runIt():
	prompt = input("Prompt : ")
	response = chat_with_chatgpt(prompt)
	print("Response: ", response)

def runPersonalAssistant():
	runIt()
	#testingIt()

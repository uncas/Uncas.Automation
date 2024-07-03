from dotenv import load_dotenv

load_dotenv()

def getTools():
	return [
		{
			"type": "function",
			"function": {
				"name": "getCurrentWeather",
				"description": "Get the current weather",
				"parameters": {
					"type": "object",
					"properties": {
						"country": {
							"type": "string",
							"description": "The country from where to get the weather"
                    	}
					}
				}
			}
		},
		{
			"type": "function",
			"function": {
				"name": "getLocation",
				"description": "Get the user's current location",
				"parameters": {
					"type": "object",
					"properties": {}
				}
			}
		},
		{
			"type": "function",
			"function": {
				"name": "getWatchProviders",
				"description": "Get watch providers for a given movie",
				"parameters": {
					"type": "object",
					"properties": {
						"movieTitle": {
							"type": "string",
							"description": "The title of the movie"
                    	}
					}
				}
			}
		},
	]

def chat_with_chatgpt(prompt, model="gpt-3.5-turbo"):
	import json
	from openai import OpenAI
	from Flows.PersonalAssistant.Functions.getLocation import getLocation
	from Flows.PersonalAssistant.Functions.getCurrentWeather import getCurrentWeather
	from Flows.PersonalAssistant.Functions.theMovieDb import getWatchProviders

	maxIterations = 3
	tools = getTools()
	toolMethods = {"getLocation": getLocation, "getCurrentWeather": getCurrentWeather, "getWatchProviders": getWatchProviders}
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
					if functionArgs:
						print("Calling function: ", functionName, " with args: ", functionArgs)
						functionResponse = toolMethods[functionName](functionArgs)
					else:
						print("Calling function: ", functionName, " without args.")
						functionResponse = toolMethods[functionName]()
					messages.append({
						"role": "tool",
						"name": functionName,
						"tool_call_id": toolCall.id,
						"content": json.dumps(functionResponse)
					})


def runPersonalAssistant():
	#prompt = "What is the weather in my current location, and in Germany and in England?"
	#print("Prompt: ", prompt)

	from Flows.PersonalAssistant.Functions.findInfoInDocs import syncDocs # type: ignore
	syncDocs()

	#prompt = input("Prompt : ")
	#response = chat_with_chatgpt(prompt)
	#print("Response: ", response)

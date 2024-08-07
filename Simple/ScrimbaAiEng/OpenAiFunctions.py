from dotenv import load_dotenv # type: ignore
load_dotenv()

def getCurrentWeather(location):
	import random
	temp = random.randint(5, 19)
	if location["country"] == "Denmark":
		return {
			"temperature": str(temp),
			"unit": "C",
			"forecast": "rainy"
		}
	return {
		"temperature": str(temp+10),
		"unit": "C",
		"forecast": "sunny"
	}

def getLocation():
	import requests
	url = "https://ipapi.co/json/"
	r = requests.get(url)
	data = r.json()
	return {
		"city": data["city"],
		"state": data["region"],
		"country": data["country_name"]
	}

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
	]

def chat_with_chatgpt(prompt, model="gpt-4o-mini"):
	from openai import OpenAI
	import json

	maxIterations = 3
	tools = getTools()
	toolMethods = {"getLocation": getLocation, "getCurrentWeather": getCurrentWeather}
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


prompt = "What is the weather in my current location, and in Germany and in England?"
print("Prompt: ", prompt)
response = chat_with_chatgpt(prompt)
print("Response: ", response)

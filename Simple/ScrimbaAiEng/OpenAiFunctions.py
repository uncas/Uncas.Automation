from dotenv import load_dotenv # type: ignore
load_dotenv()

def getCurrentWeather():
    return {
        "temperature": "75",
        "unit": "F",
        "forecast": "sunny"
    }

def getLocation():
    return "San Diego, CA"

def getTools():
	return [
		{
			"type": "function",
			"function": {
				"name": "getCurrentWeather",
				"description": "Get the current weather",
				"parameters": {
					"type": "object",
					"properties": {}
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

def chat_with_chatgpt(prompt, model="gpt-3.5-turbo", iteration = 0):
	maxIterations = 3
	if iteration >= maxIterations:
		return "Max iterations reached"
	print(prompt)
	from openai import OpenAI
	client = OpenAI()
	messages = [
		{
			"role": "user",
			"content": prompt,
		}
	]
	chat_completion = client.chat.completions.create(
		messages = messages,
		model = model,
		tools = getTools()
	)
	choice = chat_completion.choices[0]
	finishReason = choice.finish_reason
	message = choice.message
	if finishReason == "stop":
		return message.content
	elif finishReason == "tool_calls":
		callFunction = message.tool_calls[0].function
		toolMethods = {"getLocation": getLocation, "getCurrentWeather": getCurrentWeather}
		if callFunction.name in toolMethods:
			toolResult = toolMethods[callFunction.name]()
			newPrompt = f"{prompt}. The result of the {callFunction.name} function is {toolResult}."
			return chat_with_chatgpt(newPrompt, model, iteration + 1)
		else:
			return "Tool not found."


response = chat_with_chatgpt("What is the weather in my current location?")
print(response)

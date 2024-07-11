from dotenv import load_dotenv
from Flows.PersonalAssistant.Logger import foreground, background, style

load_dotenv(override = True)

def runAssistantLoop(model="gpt-3.5-turbo"):
	from openai import OpenAI
	from Flows.PersonalAssistant.AssistantTools import getTools
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
	messages = []
	while True:
		prompt = input(background.BLUE + foreground.WHITE + "You :  ")
		print(style.RESET_ALL)
		if prompt == "bye":
			printAssistantMessage("Good bye!")
			return
		messages.append({ "role": "user", "content": prompt })
		messages = runToolLoop(client, model, tools, toolMethods, messages)

def printAssistantMessage(content):
	print(background.GREEN + foreground.WHITE + "Assistant : ", content, style.RESET_ALL)

def runToolLoop(client, model, tools, toolMethods, messages):
	import json
	maxIterations = 5
	for _ in range(maxIterations):
		chatCompletion = client.chat.completions.create(
			messages = messages,
			model = model,
			tools = tools
		)
		choice = chatCompletion.choices[0]
		finishReason = choice.finish_reason
		message = choice.message
		messages.append(message)
		if finishReason == "stop":
			printAssistantMessage(message.content)
			return messages
		elif finishReason == "tool_calls":
			for toolCall in message.tool_calls:
				callFunction = toolCall.function
				if callFunction.name in toolMethods:
					functionName = callFunction.name
					functionArgs = json.loads(callFunction.arguments)
					functionResponse = None
					toolMethod = toolMethods[functionName]
					if functionArgs:
						print("Calling function", functionName, "with", functionArgs)
						functionResponse = toolMethod(functionArgs)
					else:
						print("Calling function", functionName)
						functionResponse = toolMethod()
					messages.append({
						"role": "tool",
						"name": functionName,
						"tool_call_id": toolCall.id,
						"content": json.dumps(functionResponse)
					})

def runPersonalAssistant():
	#from Flows.PersonalAssistant.TestPersonalAssistant import testIt
	#testIt()
	runAssistantLoop()

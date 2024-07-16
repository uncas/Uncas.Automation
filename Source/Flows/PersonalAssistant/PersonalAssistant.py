from dotenv import load_dotenv
from Flows.PersonalAssistant.Logger import foreground, background, style
from Flows.PersonalAssistant.Utility.AiLog import AiLog

load_dotenv(override = True)
aiLog = AiLog()

def runTaskedAgent(model = "gpt-3.5-turbo"):
	import datetime
	systemPromptFile = "TaskCalendarMailAssistant.md"
	from Flows.PersonalAssistant.Functions.getCalendarEvents import getTodaysCalendarEvents
	from Flows.PersonalAssistant.Functions.createJiraIssue import getMyJiraIssues, createJiraIssue
	from Flows.PersonalAssistant.Functions.readEmail import readEmail
	inputTasks = []
	inputTasks.append({ "task": lambda: getTodaysCalendarEvents(), "prompt": "Today's calendar events" })
	inputTasks.append({ "task": lambda: getMyJiraIssues(), "prompt": "My jira issues" })
	inputTasks.append({ "task": lambda: readEmail(), "prompt": "My mails" })
	taskSummary = "Task/Calendar/Mail assistant summary, " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
	actionOnResult = lambda result : createJiraIssue({"summary": taskSummary, "description": result})

	from openai import OpenAI
	from Flows.PersonalAssistant.AssistantTools import getTools
	import json
	toolList = getTools()
	client = OpenAI()
	messages = []
	messages.append(getSystemPrompt(systemPromptFile))
	userMessageContent = ""
	for inputTask in inputTasks:
		taskResult = json.dumps(inputTask["task"]())
		userMessageContent += inputTask["prompt"] + ": " + taskResult + "\n\n"
	messages.append(getUserPrompt(userMessageContent))
	messages = runToolLoop(client, model, toolList, messages)
	assistantMessage = messages[-1].content
	actionOnResult(assistantMessage)

def runInteractiveChatLoop(model = "gpt-3.5-turbo"):
	from openai import OpenAI
	from Flows.PersonalAssistant.AssistantTools import getTools
	toolList = getTools()
	client = OpenAI()
	messages = []
	messages.append(getSystemPrompt("InteractiveAssistantLoop.md"))
	while True:
		prompt = input(background.BLUE + foreground.WHITE + "  You        " + style.RESET_ALL + " : ")
		print()
		if prompt == "bye":
			printAssistantMessage("Good bye!")
			return
		messages.append(getUserPrompt(prompt))
		messages = runToolLoop(client, model, toolList, messages)

def getUserPrompt(content):
	return { "role": "user", "content": content }

def getSystemPrompt(fileName):
	with open("Source/Flows/PersonalAssistant/Prompts/" + fileName, "r") as file:
		systemPrompt = file.read()
		return { "role": "system", "content": systemPrompt }

def printAssistantMessage(content):
	print(background.GREEN + foreground.WHITE + "  Assistant  " + style.RESET_ALL + " :", content)
	print()

def printToolMessage(content):
	print(background.YELLOW + foreground.WHITE + "  Tool       " + style.RESET_ALL + " :", content)
	print()

def runToolLoop(client, model, toolList, messages):
	import json
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
	maxIterations = 5
	messageCountAtLastLog = len(messages) - 1
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
		aiLog.log(model, chatCompletion.usage.prompt_tokens, chatCompletion.usage.completion_tokens, messages[messageCountAtLastLog:])
		messageCountAtLastLog = len(messages)
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
						printToolMessage("Calling function " + functionName + " with " + str(functionArgs))
						functionResponse = toolMethod(functionArgs)
					else:
						printToolMessage("Calling function " + functionName)
						functionResponse = toolMethod()
					messages.append({
						"role": "tool",
						"name": functionName,
						"tool_call_id": toolCall.id,
						"content": json.dumps(functionResponse)
					})

def runPersonalAssistant():
	runInteractiveChatLoop()
	#runTaskedAgent()

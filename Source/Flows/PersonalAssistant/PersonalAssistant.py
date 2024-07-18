from dotenv import load_dotenv
from Flows.PersonalAssistant.Logger import foreground, background, style
from Flows.PersonalAssistant.Utility.AiLog import AiLog
from Flows.PersonalAssistant.Agents.AgentDefinition import AgentDefinition

load_dotenv(override = True)
aiLog = AiLog()

def runTaskedAgent(agentDefinition: AgentDefinition, model : str = "gpt-3.5-turbo"):
	from openai import OpenAI
	from Flows.PersonalAssistant.AssistantTools import getTools
	import json

	toolList = getTools()
	client = OpenAI()
	messages = []
	messages.append(getSystemPrompt(agentDefinition.systemPromptFile))
	userMessageContent = ""
	for inputTask in agentDefinition.inputTasks:
		taskResult = json.dumps(inputTask["task"]())
		userMessageContent += inputTask["prompt"] + ": " + taskResult + "\n\n"
	messages.append(getUserPrompt(userMessageContent))
	messages = runToolLoop(client, model, toolList, messages)
	assistantMessage = messages[-1].content
	agentDefinition.actionOnResult(assistantMessage)

def runInteractiveChatLoop(model = "gpt-3.5-turbo"):
	from openai import OpenAI
	from Flows.PersonalAssistant.AssistantTools import getTools
	from Utils.Settings import getSetting
	toolList = getTools()
	client = OpenAI()
	messages = []
	messages.append(getSystemPrompt("InteractiveAssistantLoop.md"))
	callName = getSetting("assistant", {}).get("callName", "You")
	while True:
		prompt = input(background.BLUE + foreground.WHITE + getRoleConsoleLine(callName) + " ")
		print()
		if prompt == "bye":
			printAssistantMessage("Good bye!")
			return
		messages.append(getUserPrompt(prompt))
		messages = runToolLoop(client, model, toolList, messages)

def getRoleConsoleLine(role : str):
	return "  " + role.ljust(11) + style.RESET_ALL + " : "

def getUserPrompt(content):
	return { "role": "user", "content": limitMessageContent(content) }

def limitMessageContent(content):
	maxMessageContentLength = 5000
	if len(content) > maxMessageContentLength:
		import logging
		logger = logging.getLogger(__name__)
		logger.warning(
			"Message content %s was too long, truncating to %d characters.",
			content[:50] + " ... " + content[-50:],
			maxMessageContentLength)
		return content[:maxMessageContentLength] + "..."
	return content

def getSystemPrompt(fileName):
	with open("Source/Flows/PersonalAssistant/Prompts/" + fileName, "r") as file:
		systemPrompt = file.read()
		return { "role": "system", "content": limitMessageContent(systemPrompt) }

def printAssistantMessage(content):
	print(background.GREEN + foreground.WHITE + getRoleConsoleLine("Assistant"), content)
	print()

def printToolMessage(content):
	print(background.YELLOW + foreground.WHITE + getRoleConsoleLine("Tool"), content)
	print()

def runToolLoop(client, model, toolList, messages):
	import json
	tools = [tool.mapToOpenAiTool() for tool in toolList]
	toolMethods = {tool.name: tool.method for tool in toolList}
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
						"content": limitMessageContent(json.dumps(functionResponse))
					})

def runPersonalAssistant():
	import logging
	from Flows.PersonalAssistant.LoggerSetup import initLogger
	initLogger()
	logger = logging.getLogger(__name__)
	logger.info("Running Personal Assistant")
	runInteractiveChatLoop()
	logger.info("Exiting Personal Assistant")

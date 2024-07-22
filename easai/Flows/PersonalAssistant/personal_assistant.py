import logging
from dotenv import load_dotenv

from openai import OpenAI

from Flows.PersonalAssistant.old_logger import foreground, background, style
from Flows.PersonalAssistant.Utility.ai_log import AiLog
from Flows.PersonalAssistant.Agents.agent_definition import AgentDefinition

defaultModel = "gpt-4o-mini"
load_dotenv(override = True)
aiLog = AiLog()

def runTaskedAgent(agent: AgentDefinition, model: str = defaultModel):
	import json

	client = OpenAI()
	messages = [getSystemPrompt(agent.system_prompt)]
	userMessageContent = ""
	for inputTask in agent.input_tasks:
		taskResult = json.dumps(inputTask["task"]())
		userMessageContent += inputTask["prompt"] + ": " + taskResult + "\n\n"
	messages.append(getUserPrompt(userMessageContent))
	messages = runToolLoop(client, model, agent.tools, messages)
	assistantMessage = messages[-1].content
	agent.action_on_result(assistantMessage)

def runInteractiveChatLoop(model = defaultModel):
	import os
	from openai import OpenAI
	from Flows.PersonalAssistant.assistant_tools import get_all_tools
	from Utils.Settings import getSetting
	if not os.getenv("OPENAI_API_KEY"):
		import logging
		logger = logging.getLogger(__name__)
		logger.critical('FATAL ERROR: OPENAI_API_KEY needed. Set the value in a .env file: echo "OPENAI_API_KEY=YOUR_API_KEY_VALUE" >> .env')
		exit(1)
	client = OpenAI()
	messages = [getSystemPromptFromFile("InteractiveAssistantLoop.md")]
	callName = getSetting("assistant", {}).get("callName", "You")
	tools = get_all_tools()
	while True:
		prompt = input(background.BLUE + foreground.WHITE + getRoleConsoleLine(callName) + " ")
		print()
		if prompt == "bye":
			printAssistantMessage("Good bye!")
			return
		messages.append(getUserPrompt(prompt))
		messages = runToolLoop(client, model, tools, messages)

def getRoleConsoleLine(role : str):
	return "  " + role.ljust(11) + style.RESET_ALL + " : "

def getUserPrompt(content):
	return { "role": "user", "content": limitMessageContent(content) }

def limitMessageContent(content):
	maxMessageContentLength = 100 * 1000
	if len(content) > maxMessageContentLength:
		import logging
		logger = logging.getLogger(__name__)
		logger.warning(
			"Message content %s was too long, truncating to %d characters.",
			content[:50] + " ... " + content[-50:],
			maxMessageContentLength)
		return content[:maxMessageContentLength] + "..."
	return content

def getSystemPrompt(systemPrompt):
	return { "role": "system", "content": limitMessageContent(systemPrompt) }

def getSystemPromptFromFile(fileName):
	with open("easai/Flows/PersonalAssistant/Prompts/" + fileName, "r") as file:
		systemPrompt = file.read()
		return getSystemPrompt(systemPrompt)

def printAssistantMessage(content):
	print(background.GREEN + foreground.WHITE + getRoleConsoleLine("Assistant"), content)
	print()

def printToolMessage(content):
	print(background.YELLOW + foreground.WHITE + getRoleConsoleLine("Tool"), content)
	print()

def runToolLoop(client: OpenAI, model: str, tools: list, messages):
	import json
	openAiTools = [tool.map_to_open_ai_tool() for tool in tools]
	toolMethods = {tool.name: tool.method for tool in tools}
	maxIterations = 10
	messageCountAtLastLog = len(messages) - 1
	for _ in range(maxIterations):
		chatCompletion = client.chat.completions.create(
			messages = messages,
			model = model,
			tools = openAiTools
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
	logger = logging.getLogger(__name__)
	logger.error("ERROR: Tool loop exited without stop reason, most likely due to too many iterations.")
	return messages

def runPersonalAssistant():
	import logging
	from Flows.PersonalAssistant.logger_setup import initLogger
	initLogger()
	logger = logging.getLogger(__name__)
	logger.info("Running Personal Assistant")
	mode = input("How can I help you? Select: 1 = Chat, 2 = Holiday planner, 3 = Blog writer : ")
	if mode == "1":
		runInteractiveChatLoop()
	elif mode == "2":
		from Flows.PersonalAssistant.Agents.activity_planner_agent import ActivityPlannerAgent
		runTaskedAgent(ActivityPlannerAgent())
	elif mode == "3":
		from Flows.PersonalAssistant.Agents.blog_writer_agent import BlogWriterAgent
		runTaskedAgent(BlogWriterAgent())
	logger.info("Exiting Personal Assistant")

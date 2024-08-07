import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

from easai.assistant.assistant_tools import get_all_tools
from easai.assistant.logger_setup import init_logger
from easai.assistant.old_logger import foreground, background, style
from easai.assistant.Agents.activity_planner_agent import ActivityPlannerAgent
from easai.assistant.Agents.agent_definition import AgentDefinition
from easai.assistant.Agents.blog_writer_agent import BlogWriterAgent
from easai.assistant.Utility.ai_log import AiLog
from easai.Utils.Settings import getSetting

load_dotenv(override = True)
aiLog = AiLog()

def get_llm_type() -> str:
	value = os.getenv("LlmType")
	if not value:
		return "Ollama"
	return value

def get_llm_client() -> OpenAI:
	llmType = get_llm_type()
	if llmType == "OpenAi":
		return OpenAI()
	return OpenAI(base_url='http://localhost:11434/v1/', api_key='ollama')

def get_llm_model() -> str:
	model = os.getenv("LlmModel")
	if model and len(model) > 0:
		return model
	
	llmType = get_llm_type()
	if llmType == "OpenAi":
		return "gpt-4o-mini"
	return "sam4096/qwen2tools:1.5b"

def run_tasked_agent(agent: AgentDefinition):
	client = get_llm_client()
	messages = [getSystemPrompt(agent.system_prompt)]
	user_message_content = ""
	for inputTask in agent.input_tasks:
		taskResult = json.dumps(inputTask["task"]())
		user_message_content += inputTask["prompt"] + ": " + taskResult + "\n\n"
	messages.append(getUserPrompt(user_message_content))
	messages = runToolLoop(client, agent.tools, messages)
	assistantMessage = messages[-1].content
	agent.action_on_result(assistantMessage)

def runInteractiveChatLoop():
	if not os.getenv("OPENAI_API_KEY"):
		logger = logging.getLogger(__name__)
		logger.critical('FATAL ERROR: OPENAI_API_KEY needed. Set the value in a .env file: echo "OPENAI_API_KEY=YOUR_API_KEY_VALUE" >> .env')
		exit(1)
	client = get_llm_client()
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
		messages = runToolLoop(client, tools, messages)

def getRoleConsoleLine(role : str):
	return "  " + role.ljust(11) + style.RESET_ALL + " : "

def getUserPrompt(content):
	return { "role": "user", "content": limitMessageContent(content) }

def limitMessageContent(content):
	maxMessageContentLength = 100 * 1000
	if len(content) > maxMessageContentLength:
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
	with open("easai/assistant/Prompts/" + fileName, "r") as file:
		systemPrompt = file.read()
		return getSystemPrompt(systemPrompt)

def printAssistantMessage(content):
	print(background.GREEN + foreground.WHITE + getRoleConsoleLine("Assistant"), content)
	print()

def printToolMessage(content):
	print(background.YELLOW + foreground.WHITE + getRoleConsoleLine("Tool"), content)
	print()

def runToolLoop(client: OpenAI, tools: list, messages):
	openAiTools = [tool.map_to_open_ai_tool() for tool in tools]
	toolMethods = {tool.name: tool.method for tool in tools}
	maxIterations = 10
	messageCountAtLastLog = len(messages) - 1
	model = get_llm_model()
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
	init_logger()
	logger = logging.getLogger(__name__)
	logger.info("Running Personal Assistant")
	mode = input("How can I help you? Select: 1 = Chat, 2 = Holiday planner, 3 = Blog writer : ")
	if mode == "1":
		runInteractiveChatLoop()
	elif mode == "2":
		run_tasked_agent(ActivityPlannerAgent())
	elif mode == "3":
		run_tasked_agent(BlogWriterAgent())
	logger.info("Exiting Personal Assistant")

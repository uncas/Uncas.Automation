import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

from uncas_automation.assistant.assistant_tools import get_all_tools
from uncas_automation.assistant.logger_setup import init_logger
from uncas_automation.assistant.old_logger import foreground, background, style
from uncas_automation.assistant.Agents.activity_planner_agent import ActivityPlannerAgent
from uncas_automation.assistant.Agents.agent_definition import AgentDefinition
from uncas_automation.assistant.Agents.blog_writer_agent import BlogWriterAgent
from uncas_automation.assistant.Agents.coding_agent import CodingAgent
from uncas_automation.assistant.Utility.ai_log import AiLog
from uncas_automation.Utils.Settings import getSetting

load_dotenv(override = True)
ai_log = AiLog()

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
	messages = [get_system_prompt(agent.system_prompt)]
	user_message_content = ""
	for inputTask in agent.input_tasks:
		taskResult = json.dumps(inputTask["task"]())
		user_message_content += inputTask["prompt"] + ": " + taskResult + "\n\n"
	messages.append(get_user_prompt(user_message_content))
	messages = run_tool_loop(client, agent.tools, messages)
	assistantMessage = messages[-1].content
	agent.action_on_result(assistantMessage)

def run_chat_loop():
	if not os.getenv("OPENAI_API_KEY"):
		logger = logging.getLogger(__name__)
		logger.critical('FATAL ERROR: OPENAI_API_KEY needed. Set the value in a .env file: echo "OPENAI_API_KEY=YOUR_API_KEY_VALUE" >> .env')
		exit(1)
	client = get_llm_client()
	messages = [read_system_prompt_file("InteractiveAssistantLoop.md")]
	callName = getSetting("assistant", {}).get("callName", "You")
	tools = get_all_tools()
	while True:
		prompt = input(background.BLUE + foreground.WHITE + get_role_console_line(callName) + " ")
		print()
		if prompt == "bye":
			print_assistant_message("Good bye!")
			return
		messages.append(get_user_prompt(prompt))
		messages = run_tool_loop(client, tools, messages)

def get_role_console_line(role : str):
	return "  " + role.ljust(11) + style.RESET_ALL + " : "

def get_user_prompt(content):
	return { "role": "user", "content": get_limited_message_content(content) }

def get_limited_message_content(content):
	maxMessageContentLength = 100 * 1000
	if len(content) > maxMessageContentLength:
		logger = logging.getLogger(__name__)
		logger.warning(
			"Message content %s was too long, truncating to %d characters.",
			content[:50] + " ... " + content[-50:],
			maxMessageContentLength)
		return content[:maxMessageContentLength] + "..."
	return content

def get_system_prompt(systemPrompt):
	return { "role": "system", "content": get_limited_message_content(systemPrompt) }

def read_system_prompt_file(file_name):
	with open("uncas_automation/assistant/Prompts/" + file_name, "r") as file:
		system_prompt = file.read()
		return get_system_prompt(system_prompt)

def print_assistant_message(content):
	print(background.GREEN + foreground.WHITE + get_role_console_line("Assistant"), content)
	print()

def print_tool_message(content):
	print(background.YELLOW + foreground.WHITE + get_role_console_line("Tool"), content)
	print()

def run_tool_loop(client: OpenAI, tools: list, messages):
	client_tools = [tool.map_to_open_ai_tool() for tool in tools]
	tool_methods = {tool.name: tool.method for tool in tools}
	max_iterations = 10
	message_count_at_last_log = len(messages) - 1
	model = get_llm_model()
	for _ in range(max_iterations):
		chat_completion = client.chat.completions.create(
			messages = messages,
			model = model,
			tools = client_tools
		)
		choice = chat_completion.choices[0]
		finish_reason = choice.finish_reason
		message = choice.message
		messages.append(message)
		ai_log.log(model, chat_completion.usage.prompt_tokens, chat_completion.usage.completion_tokens, messages[message_count_at_last_log:])
		message_count_at_last_log = len(messages)
		if finish_reason == "stop":
			print_assistant_message(message.content)
			return messages
		elif finish_reason == "tool_calls":
			for tool_call in message.tool_calls:
				call_function = tool_call.function
				if call_function.name in tool_methods:
					function_name = call_function.name
					function_args = json.loads(call_function.arguments)
					function_response = None
					tool_method = tool_methods[function_name]
					if function_args:
						print_tool_message("Calling function " + function_name + " with " + str(function_args))
						function_response = tool_method(function_args)
					else:
						print_tool_message("Calling function " + function_name)
						function_response = tool_method()
					messages.append({
						"role": "tool",
						"name": function_name,
						"tool_call_id": tool_call.id,
						"content": get_limited_message_content(json.dumps(function_response))
					})
	logger = logging.getLogger(__name__)
	logger.error("ERROR: Tool loop exited without stop reason, most likely due to too many iterations.")
	return messages

def run_personal_assistant():
	init_logger()
	logger = logging.getLogger(__name__)
	logger.info("Running Personal Assistant")
	mode = input("How can I help you? Select: 1 = Chat, 2 = Holiday planner, 3 = Blog writer, 4 = Coder : ")
	if mode == "1":
		run_chat_loop()
	elif mode == "2":
		run_tasked_agent(ActivityPlannerAgent())
	elif mode == "3":
		run_tasked_agent(BlogWriterAgent())
	elif mode == "4":
		run_tasked_agent(CodingAgent())
	logger.info("Exiting Personal Assistant")

import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

from easai.assistant.log import SqliteAiLog
from easai.assistant.loop import run_tool_loop, get_system_prompt, get_user_prompt
from easai.assistant.chat_console import run_chat_console, print_assistant_message, print_tool_message

from uncas_automation.assistant.assistant_tools import get_all_tools
from uncas_automation.assistant.logger_setup import init_logger
from uncas_automation.assistant.Agents.activity_planner_agent import ActivityPlannerAgent
from uncas_automation.assistant.Agents.agent_definition import AgentDefinition
from uncas_automation.assistant.Agents.blog_writer_agent import BlogWriterAgent
from uncas_automation.assistant.Agents.coding_agent import CodingAgent
from uncas_automation.Utils.Settings import getSetting

load_dotenv(override = True)
ai_log = SqliteAiLog("Data/AiLog.db")

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
	messages = run_tool_loop_here(client, agent.tools, messages)
	assistantMessage = messages[-1].content
	agent.action_on_result(assistantMessage)

def run_chat_loop():
	if not os.getenv("OPENAI_API_KEY"):
		logger = logging.getLogger(__name__)
		logger.critical('FATAL ERROR: OPENAI_API_KEY needed. Set the value in a .env file: echo "OPENAI_API_KEY=YOUR_API_KEY_VALUE" >> .env')
		exit(1)
	run_chat_console(
		client = get_llm_client(), 
		model = get_llm_model(),
		system_prompt = read_system_prompt_file("InteractiveAssistantLoop.md"),
		your_name = getSetting("assistant", {}).get("callName", "You"),
		tools = get_all_tools(),
		ai_logger = ai_log)

def read_system_prompt_file(file_name):
	with open("uncas_automation/assistant/Prompts/" + file_name, "r") as file:
		return file.read()

def run_tool_loop_here(client: OpenAI, tools: list, messages: list):
	return run_tool_loop(
		client,
		tools,
		messages,
		model = get_llm_model(),
		max_iterations = 10,
		assistant_message_callback = print_assistant_message,
		tool_message_callback = print_tool_message,
		ai_logger = ai_log)

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

import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

from easai.assistant.log import SqliteAiLog
from easai.assistant.assistant import run_assistant, get_user_prompt, Assistant
from easai.assistant.chat_console import run_chat_console, print_assistant_message, print_tool_message
from easai.assistant.tools.coding_tool import CodingTool

from uncas_automation.assistant.Functions.read_web_page import read_web_page_text_tool
from uncas_automation.assistant.Functions.search_internet import search_internet_tool
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
	user_message_content = ""
	for inputTask in agent.input_tasks:
		taskResult = json.dumps(inputTask["task"]())
		user_message_content += inputTask["prompt"] + ": " + taskResult + "\n\n"
	messages = [get_user_prompt(user_message_content)]
	assistant = Assistant(
		client = get_llm_client(), 
		model = get_llm_model(),
		system_prompt = agent.system_prompt,
		tools = agent.tools,
		max_iterations = 10)
	messages = run_assistant(
		messages = messages,
		assistant = assistant,
		assistant_message_callback = print_assistant_message,
		tool_message_callback = print_tool_message,
		ai_logger = ai_log)
	assistantMessage = messages[-1].content
	agent.action_on_result(assistantMessage)

def run_chat_loop():
	if not os.getenv("OPENAI_API_KEY"):
		logger = logging.getLogger(__name__)
		logger.critical('FATAL ERROR: OPENAI_API_KEY needed. Set the value in a .env file: echo "OPENAI_API_KEY=YOUR_API_KEY_VALUE" >> .env')
		exit(1)
	assistant = Assistant(
		client = get_llm_client(), 
		model = get_llm_model(),
		system_prompt = read_system_prompt_file("InteractiveAssistantLoop.md"),
		tools = get_all_tools())
	run_chat_console(
		assistant = assistant,
		your_name = getSetting("assistant", {}).get("callName", "You"),
		ai_logger = ai_log)

def run_repo_coding_loop(path_to_code: str):
	tools = CodingTool(path_to_code, approve_execution = True).get_all_tools()
	tools.append(read_web_page_text_tool())
	tools.append(search_internet_tool())
	system_prompt="You are a good software developer working a repository to which you have access to the files. You make small changes at a time, respecting the existing functionality of the project."
	assistant = Assistant(
		client = get_llm_client(), 
		model = get_llm_model(),
		system_prompt = system_prompt,
		tools = tools)
	run_chat_console(
		assistant = assistant,
		your_name = getSetting("assistant", {}).get("callName", "You"),
		ai_logger = ai_log)

def read_system_prompt_file(file_name):
	with open("uncas_automation/assistant/Prompts/" + file_name, "r") as file:
		return file.read()

def run_personal_assistant():
	init_logger()
	logger = logging.getLogger(__name__)
	logger.info("Running Personal Assistant")
	mode = input("How can I help you? Select: 1 = Chat, 2 = Holiday planner, 3 = Blog writer, 4 = Coder, 5 = Code on uncas.dk, 6 = Code on easai : ")
	if mode == "1":
		run_chat_loop()
	elif mode == "2":
		run_tasked_agent(ActivityPlannerAgent())
	elif mode == "3":
		run_tasked_agent(BlogWriterAgent())
	elif mode == "4":
		run_tasked_agent(CodingAgent())
	elif mode == "5":
		run_repo_coding_loop("../uncas.dk")
	elif mode == "6":
		run_repo_coding_loop("../easai")
	logger.info("Exiting Personal Assistant")

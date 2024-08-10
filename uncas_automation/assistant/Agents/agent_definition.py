from easai.assistant.tool import AssistantTool

class AgentDefinition:
	def __init__(self, system_prompt: str, input_tasks, action_on_result, tools: list[AssistantTool] = []):
		self.system_prompt = system_prompt
		self.input_tasks = input_tasks
		self.action_on_result = action_on_result
		self.tools: list[AssistantTool] = tools

	def get_system_prompt_from_file(file_name):
		with open("uncas_automation/assistant/Prompts/" + file_name, "r") as file:
			return file.read()

	def write_output_to_file(self, file_prefix, output):
		from easai.utils.file_utils import write_text
		import datetime
		date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
		file_name = file_prefix + "_" + date_string + ".md"
		write_text("Output", file_name, output)
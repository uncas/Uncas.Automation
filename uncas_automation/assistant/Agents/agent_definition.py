class AgentDefinition:
	def __init__(self, system_prompt, input_tasks, action_on_result, tools = []):
		self.system_prompt = system_prompt
		self.input_tasks = input_tasks
		self.action_on_result = action_on_result
		self.tools = tools

	def get_system_prompt_from_file(file_name):
		with open("uncas_automation/assistant/Prompts/" + file_name, "r") as file:
			return file.read()

	def write_output_to_file(self, file_prefix, output):
		from uncas_automation.Utils.FileUtils import write_text
		import datetime
		date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
		file_name = file_prefix + "_" + date_string + ".md"
		write_text("Output", file_name, output)
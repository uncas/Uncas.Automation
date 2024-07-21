class AgentDefinition:
	def __init__(self, systemPrompt, inputTasks, actionOnResult, tools = []):
		self.systemPrompt = systemPrompt
		self.inputTasks = inputTasks
		self.actionOnResult = actionOnResult
		self.tools = tools

	def get_system_prompt_from_file(fileName):
		with open("Source/Flows/PersonalAssistant/Prompts/" + fileName, "r") as file:
			return file.read()

	def write_output_to_file(self, file_prefix, output):
		from Utils.FileUtils import writeText
		import datetime
		dateString = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
		fileName = file_prefix + "_" + dateString + ".md"
		writeText("Output", fileName, output)
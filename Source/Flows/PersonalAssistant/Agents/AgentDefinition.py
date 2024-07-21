class AgentDefinition:
	def __init__(self, systemPrompt, inputTasks, actionOnResult, tools = []):
		self.systemPrompt = systemPrompt
		self.inputTasks = inputTasks
		self.actionOnResult = actionOnResult
		self.tools = tools

	def getSystemPromptFromFile(fileName):
		with open("Source/Flows/PersonalAssistant/Prompts/" + fileName, "r") as file:
			return file.read()

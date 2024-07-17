class AgentDefinition:
	def __init__(self, systemPromptFile, inputTasks, actionOnResult):
		self.systemPromptFile = systemPromptFile
		self.inputTasks = inputTasks
		self.actionOnResult = actionOnResult

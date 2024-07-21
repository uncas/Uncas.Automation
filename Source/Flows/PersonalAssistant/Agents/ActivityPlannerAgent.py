from Flows.PersonalAssistant.Agents.AgentDefinition import AgentDefinition

class ActivityPlannerAgent(AgentDefinition):
	def __init__(self):
		import os
		userPromptFile = "Data/Prompts/HolidayActivityPlanner-user.md"
		if not os.path.exists(userPromptFile):
			import logging
			logger = logging.getLogger(__name__)
			userPromptExampleFile = "Source/Flows/PersonalAssistant/Prompts/HolidayActivityPlanner-user.md"
			logger.critical("User prompt file not found at " + userPromptFile + 
				   ". You can see an example prompt file here, that you could copy and modify: " + userPromptExampleFile)
			exit(1)
		scenario = open(userPromptFile, "r").read()
		systemPromptFile = "HolidayActivityPlanner-system.md"
		systemPrompt = AgentDefinition.getSystemPromptFromFile(systemPromptFile)
		inputTasks = []
		inputTasks.append({ "task": lambda: scenario, "prompt": "The scenario for the activities" })
		actionOnResult = self.writePlan
		super().__init__(systemPrompt, inputTasks, actionOnResult, tools = self.getTools())

	def writePlan(self, plan):
		from Utils.FileUtils import writeText
		import datetime
		dateString = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
		fileName = "HolidayPlan-" + dateString + ".md"
		writeText("Output", fileName, plan)
	
	def getTools(self):
		from Flows.PersonalAssistant.Functions.getCurrentWeather import getCurrentWeatherTool
		from Flows.PersonalAssistant.Functions.getDateAndTime import getDateAndTimeTool
		from Flows.PersonalAssistant.Functions.getLocation import getLocationTool
		from Flows.PersonalAssistant.Functions.getTravelDirections import getTravelDirectionsTool
		from Flows.PersonalAssistant.Functions.getLatestNews import getLatestNewsTool, getNewsDetailsTool
		from Flows.PersonalAssistant.Functions.readWebPage import readWebPageTool
		from Flows.PersonalAssistant.Functions.search_wikipedia import search_wikipedia_tool
		from Flows.PersonalAssistant.Functions.search_internet import search_internet_tool

		return [
			getCurrentWeatherTool(),
			getDateAndTimeTool(),
			getLatestNewsTool(),
			getLocationTool(),
			getNewsDetailsTool(),
			getTravelDirectionsTool(),
			readWebPageTool(),
			search_wikipedia_tool(),
			search_internet_tool()
		]

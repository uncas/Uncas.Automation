from Flows.PersonalAssistant.Agents.agent_definition import AgentDefinition

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
		systemPrompt = AgentDefinition.get_system_prompt_from_file(systemPromptFile)
		inputTasks = []
		inputTasks.append({ "task": lambda: scenario, "prompt": "The scenario for the activities" })
		actionOnResult = lambda plan : super().write_output_to_file("HolidayPlan", plan)
		super().__init__(systemPrompt, inputTasks, actionOnResult, tools = self.getTools())

	def getTools(self):
		from Flows.PersonalAssistant.Functions.query_weather import get_current_weather_tool
		from Flows.PersonalAssistant.Functions.query_date_and_time import get_date_and_time_tool
		from Flows.PersonalAssistant.Functions.query_location import get_location_tool
		from Flows.PersonalAssistant.Functions.get_travel_directions import get_travel_directions_tool
		from Flows.PersonalAssistant.Functions.get_latest_news import get_latest_news_tool, get_news_details_tool
		from Flows.PersonalAssistant.Functions.read_web_page import read_web_page_text_tool
		from Flows.PersonalAssistant.Functions.search_wikipedia import search_wikipedia_tool
		from Flows.PersonalAssistant.Functions.search_internet import search_internet_tool

		return [
			get_current_weather_tool(),
			get_date_and_time_tool(),
			get_latest_news_tool(),
			get_location_tool(),
			get_news_details_tool(),
			get_travel_directions_tool(),
			read_web_page_text_tool(),
			search_wikipedia_tool(),
			search_internet_tool()
		]

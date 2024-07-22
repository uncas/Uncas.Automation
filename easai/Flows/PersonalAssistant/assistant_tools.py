class AssistantToolParameter:
	def __init__(self, name: str, description: str, type: str = "string", enum: list[str] = None):
		self.name = name
		self.description = description
		self.type = type
		self.enum = enum
	
	def get_open_ai_tool_properties(self) -> dict:
		value = {
			"type": self.type,
			"description": self.description
		}
		if self.enum:
			value["enum"] = self.enum
		return value

class AssistantTool:
	def __init__(self, method, description: str, parameters: list[AssistantToolParameter] = [], name: str = None):
		self.parameters: list[AssistantToolParameter] = parameters
		self.description = description
		self.method = method
		self.name = name if name else method.__name__
	
	def map_to_open_ai_tool(self) -> dict:
		properties = {}
		for parameter in self.parameters:
			properties[parameter.name] = parameter.get_open_ai_tool_properties()
		return {
			"type": "function",
			"function": {
				"name": self.name,
				"description": self.description,
				"parameters": {
					"type": "object",
					"properties": properties
				}
			}
		}

def get_all_tools():
	from Flows.PersonalAssistant.Functions.manage_jira import create_jira_issue_tool, get_my_jira_issues_tool
	from Flows.PersonalAssistant.Functions.manage_calendar import get_todays_calendar_events_tool
	from Flows.PersonalAssistant.Functions.query_weather import get_current_weather_tool
	from Flows.PersonalAssistant.Functions.query_date_and_time import get_date_and_time_tool
	from Flows.PersonalAssistant.Functions.query_location import get_location_tool
	from Flows.PersonalAssistant.Functions.get_travel_directions import get_travel_directions_tool
	from Flows.PersonalAssistant.Functions.find_info_in_docs import find_info_in_docs_tool
	from Flows.PersonalAssistant.Functions.get_latest_news import get_latest_news_tool, get_news_details_tool
	from Flows.PersonalAssistant.Functions.read_email import read_email_tool, write_email_tool
	from Flows.PersonalAssistant.Functions.read_web_page import read_web_page_text_tool, read_web_page_markdown_tool
	from Flows.PersonalAssistant.Functions.search_arxiv import search_arxiv_tool
	from Flows.PersonalAssistant.Functions.movie_database import get_watch_providers_tool, get_unwatched_good_watchable_movies_tool
	from Flows.PersonalAssistant.Resources.resource_tools import get_resource_tools
	from Flows.PersonalAssistant.Functions.search_wikipedia import search_wikipedia_tool
	from Flows.PersonalAssistant.Functions.search_internet import search_internet_tool, find_images_tool
	from Flows.PersonalAssistant.Functions.ask_user import ask_user_tool

	tools = [
		ask_user_tool(),
		create_jira_issue_tool(),
		find_info_in_docs_tool(),
		find_images_tool(),
		get_current_weather_tool(),
		get_date_and_time_tool(),
		get_latest_news_tool(),
		get_location_tool(),
		get_my_jira_issues_tool(),
		get_news_details_tool(),
		get_todays_calendar_events_tool(),
		get_travel_directions_tool(),
		get_unwatched_good_watchable_movies_tool(),
		get_watch_providers_tool(),
		read_email_tool(),
		read_web_page_markdown_tool(),
		read_web_page_text_tool(),
		search_internet_tool(),
		search_wikipedia_tool(),
		search_arxiv_tool(),
		write_email_tool()
	]

	for tool in get_resource_tools():
		tools.append(tool)

	return tools

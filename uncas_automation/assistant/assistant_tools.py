def get_all_tools():
	from uncas_automation.assistant.Functions.manage_jira import create_jira_issue_tool, get_my_jira_issues_tool
	from uncas_automation.assistant.Functions.manage_calendar import get_todays_calendar_events_tool
	from uncas_automation.assistant.Functions.query_weather import get_current_weather_tool
	from uncas_automation.assistant.Functions.query_date_and_time import get_date_and_time_tool
	from uncas_automation.assistant.Functions.query_location import get_location_tool
	from uncas_automation.assistant.Functions.get_travel_directions import get_travel_directions_tool
	from uncas_automation.assistant.Functions.find_info_in_docs import find_info_in_docs_tool
	from uncas_automation.assistant.Functions.get_latest_news import get_latest_news_tool, get_news_details_tool
	from uncas_automation.assistant.Functions.read_email import read_email_tool, write_email_tool
	from uncas_automation.assistant.Functions.read_web_page import read_web_page_text_tool, read_web_page_markdown_tool
	from uncas_automation.assistant.Functions.search_arxiv import search_arxiv_tool
	from uncas_automation.assistant.Functions.movie_database import get_watch_providers_tool, get_unwatched_good_watchable_movies_tool
	from uncas_automation.assistant.Resources.resource_tools import get_resource_tools
	from uncas_automation.assistant.Functions.search_wikipedia import search_wikipedia_tool
	from uncas_automation.assistant.Functions.search_internet import search_internet_tool, find_images_tool
	from uncas_automation.assistant.Functions.ask_user import ask_user_tool
	from uncas_automation.assistant.Functions.save_to_file import save_to_file_tool

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
		save_to_file_tool(),
		search_internet_tool(),
		search_wikipedia_tool(),
		search_arxiv_tool(),
		write_email_tool()
	]

	for tool in get_resource_tools():
		tools.append(tool)

	return tools

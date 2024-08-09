def search_internet(data):
	from uncas_automation.Services.internet_search_service import search_internet
	query = data["query"]
	top_results_to_return = data["top_results_to_return"] if "top_results_to_return" in data else 5
	country_code = data["country_code"] if "country_code" in data else "dk"
	language_code = data["language_code"] if "language_code" in data else "da"
	return list(search_internet(query, top_results_to_return, country_code, language_code))

def search_internet_tool():
	from uncas_automation.assistant.assistant_tools import AssistantTool, AssistantToolParameter
	return AssistantTool(search_internet, "Query a search engine for matching web pages", [
		AssistantToolParameter("query", "The thing to find pages about"),
		AssistantToolParameter("top_results_to_return", "The number of results to return (optional, defaults to 5)", type = "integer"),
		AssistantToolParameter("country_code", "The country code to search in (optional, defaults to 'dk')"),
		AssistantToolParameter("language_code", "The language code to search in (optional, defaults to 'da')")
	]
)

def find_images(data):
	from uncas_automation.Services.internet_search_service import find_images
	query = data["query"]
	top_results_to_return = data["top_results_to_return"] if "top_results_to_return" in data else 5
	country_code = data["country_code"] if "country_code" in data else "dk"
	language_code = data["language_code"] if "language_code" in data else "da"
	return list(find_images(query, top_results_to_return, country_code, language_code))

def find_images_tool():
	from uncas_automation.assistant.assistant_tools import AssistantTool, AssistantToolParameter
	return AssistantTool(find_images, "Query a search engine for matching images", [
		AssistantToolParameter("query", "The thing to find images about"),
		AssistantToolParameter("top_results_to_return", "The number of results to return (optional, defaults to 5)", type = "integer"),
		AssistantToolParameter("country_code", "The country code to search in (optional, defaults to 'dk')"),
		AssistantToolParameter("language_code", "The language code to search in (optional, defaults to 'da')")
	]
)
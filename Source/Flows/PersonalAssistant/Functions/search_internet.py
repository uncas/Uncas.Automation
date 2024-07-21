def search_internet(data):
	from Services.internet_search_service import search_internet
	query = data["query"]
	top_results_to_return = data["top_results_to_return"] if "top_results_to_return" in data else 5
	country_code = data["country_code"] if "country_code" in data else "dk"
	language_code = data["language_code"] if "language_code" in data else "da"
	return list(search_internet(query, top_results_to_return, country_code, language_code))

def search_internet_tool():
	from Flows.PersonalAssistant.AssistantTools import AssistantTool, AssistantToolParameter
	return AssistantTool(search_internet, "search_internet", [
		AssistantToolParameter("query", "The thing to search for in the internet"),
		AssistantToolParameter("top_results_to_return", "The number of results to return (optional, defaults to 5)", type = "integer"),
		AssistantToolParameter("country_code", "The country code to search in (optional, defaults to 'dk')"),
		AssistantToolParameter("language_code", "The language code to search in (optional, defaults to 'da')")
	]
)
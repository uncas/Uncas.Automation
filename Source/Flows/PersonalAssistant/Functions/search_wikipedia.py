def search_wikipedia(data):
	from Services.wikipedia_service import search_wikipedia_langchain
	query = data["query"]
	return search_wikipedia_langchain(query)

def search_wikipedia_tool():
	from Flows.PersonalAssistant.AssistantTools import AssistantTool, AssistantToolParameter
	return AssistantTool(search_wikipedia, "search_wikipedia", [
		AssistantToolParameter("query", "The thing to search for in the wikipedia")
	]
)
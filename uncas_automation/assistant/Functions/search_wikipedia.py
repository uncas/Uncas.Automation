def search_wikipedia(query):
	from uncas_automation.Services.wikipedia_service import search_wikipedia_langchain
	return search_wikipedia_langchain(query)

def search_wikipedia_tool():
	from easai.assistant.tool import AssistantTool, AssistantToolParameter
	return AssistantTool(search_wikipedia, "search_wikipedia", [
		AssistantToolParameter("query", "The thing to search for in the wikipedia")
	]
)
def readWebPage(data):
	from Services.web_page_reader import read_web_page
	url = data["url"]
	return read_web_page(url)

def read_web_page_tool():
	from Flows.PersonalAssistant.AssistantTools import AssistantTool, AssistantToolParameter
	return AssistantTool(readWebPage, "Read web page", [
		AssistantToolParameter("url", "The url of the web page")
	])
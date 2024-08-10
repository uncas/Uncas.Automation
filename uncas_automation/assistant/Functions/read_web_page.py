def read_web_page_text(url):
	from uncas_automation.Services.web_page_reader import read_web_page_text
	return read_web_page_text(url)

def read_web_page_text_tool():
	from easai.assistant.tool import AssistantTool, AssistantToolParameter
	return AssistantTool(read_web_page_text, "Read the text from a web page", [
		AssistantToolParameter("url", "The url of the web page")
	])

def read_web_page_markdown(url):
	from uncas_automation.Services.web_page_reader import read_web_page_markdown
	return read_web_page_markdown(url)

def read_web_page_markdown_tool():
	from easai.assistant.tool import AssistantTool, AssistantToolParameter
	return AssistantTool(read_web_page_markdown, "Read the text and links and images from a web page, as markdown; this can be useful for diving deeper into links or for reusing images.", [
		AssistantToolParameter("url", "The url of the web page")
	])
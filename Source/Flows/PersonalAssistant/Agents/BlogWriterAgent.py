from Flows.PersonalAssistant.Agents.AgentDefinition import AgentDefinition

class BlogWriterAgent(AgentDefinition):
	def __init__(self):
		systemPromptFile = "BlogWriter-system.md"
		systemPrompt = AgentDefinition.getSystemPromptFromFile(systemPromptFile)
		inputTasks = []
		scenario = input("What should I blog about?")
		inputTasks.append({ "task": lambda: scenario, "prompt": "The context for the blog post" })
		actionOnResult = self.write_blog_post_to_file
		super().__init__(systemPrompt, inputTasks, actionOnResult, tools = self.get_tools())

	def write_blog_post_to_file(self, output):
		super().write_output_to_file("BlogPost", output)

	def get_tools(self):
		from Flows.PersonalAssistant.Functions.getLatestNews import get_latest_news_tool, get_news_details_tool
		from Flows.PersonalAssistant.Functions.readWebPage import read_web_page_tool
		from Flows.PersonalAssistant.Functions.search_wikipedia import search_wikipedia_tool
		from Flows.PersonalAssistant.Functions.search_internet import search_internet_tool
		from Flows.PersonalAssistant.Functions.searchArxiv import search_arxiv_tool
		from Flows.PersonalAssistant.Functions.ask_user import ask_user_tool

		return [
			ask_user_tool(),
			get_latest_news_tool(),
			get_news_details_tool(),
			read_web_page_tool(),
			search_arxiv_tool(),
			search_wikipedia_tool(),
			search_internet_tool()
		]

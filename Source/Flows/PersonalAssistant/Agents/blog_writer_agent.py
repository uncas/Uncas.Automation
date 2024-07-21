from Flows.PersonalAssistant.Agents.agent_definition import AgentDefinition

class BlogWriterAgent(AgentDefinition):
	def __init__(self):
		system_prompt_file = "BlogWriter-system.md"
		system_prompt = AgentDefinition.get_system_prompt_from_file(system_prompt_file)
		input_tasks = []
		scenario = input("What should I blog about?")
		input_tasks.append({ "task": lambda: scenario, "prompt": "The context for the blog post" })
		action_on_result = self.write_blog_post_to_file
		super().__init__(system_prompt, input_tasks, action_on_result, tools = self.get_tools())

	def write_blog_post_to_file(self, output):
		super().write_output_to_file("BlogPost", output)

	def get_tools(self):
		from Flows.PersonalAssistant.Functions.get_latest_news import get_latest_news_tool, get_news_details_tool
		from Flows.PersonalAssistant.Functions.read_web_page import read_web_page_text_tool, read_web_page_markdown_tool
		from Flows.PersonalAssistant.Functions.search_internet import find_images_tool
		from Flows.PersonalAssistant.Functions.search_internet import search_internet_tool
		from Flows.PersonalAssistant.Functions.search_wikipedia import search_wikipedia_tool
		from Flows.PersonalAssistant.Functions.search_arxiv import search_arxiv_tool
		from Flows.PersonalAssistant.Functions.ask_user import ask_user_tool

		return [
			ask_user_tool(),
			find_images_tool(),
			get_latest_news_tool(),
			get_news_details_tool(),
			read_web_page_markdown_tool(),
			read_web_page_text_tool(),
			search_arxiv_tool(),
			search_wikipedia_tool(),
			search_internet_tool()
		]

def search_wikipedia_langchain(query):
	from langchain_community.tools import WikipediaQueryRun
	from langchain_community.utilities import WikipediaAPIWrapper
	wikipedia = WikipediaQueryRun(api_wrapper = WikipediaAPIWrapper())
	return wikipedia.run(query)

def search_wikipedia(query):
	import wikipedia
	pages = wikipedia.search(query)
	page = pages[0]
	return wikipedia.summary(page, sentences = 10)

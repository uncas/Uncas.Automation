from typing import Generator

def search_internet(query: str, top_results_to_return = 5, country_code = "dk", language_code = "da") -> Generator:
	"""Useful to search the internet
	about a a given topic and return relevant results"""

	from duckduckgo_search import DDGS

	region = country_code + "-" + language_code
	results = DDGS().text(query, max_results = top_results_to_return, region = region)
	for result in results:
		yield {"title": result["title"], "href": result["href"], "body": result["body"]}

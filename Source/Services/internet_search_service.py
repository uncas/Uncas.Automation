from typing import Generator

def search_internet(query: str, top_results_to_return = 5, country_code = "dk", language_code = "da") -> Generator:
	"""Useful to search the internet
	about a a given topic and return relevant results"""

	from duckduckgo_search import DDGS

	region = country_code + "-" + language_code
	DDGS().images(keywords=query, max_results = top_results_to_return, region = region)
	results = DDGS().text(query, max_results = top_results_to_return, region = region)
	for result in results:
		yield {"title": result["title"], "href": result["href"], "body": result["body"]}

def find_images(query: str, top_results_to_return = 5, country_code = "dk", language_code = "da") -> Generator:
	"""Useful to fin image from the internet
	about a a given topic and return relevant results"""

	from duckduckgo_search import DDGS

	region = country_code + "-" + language_code
	results = DDGS().images(keywords=query, max_results = top_results_to_return, region = region)
	for result in results:
		yield {
			"page_title": result["title"], 
			"image_url": result["image"], 
			"thumbnail_url": result["thumbnail"],
			"page_url": result["url"], 
		 	"height": result["height"],
		   	"width": result["width"]
		}

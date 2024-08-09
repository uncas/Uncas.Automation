def searchArxiv(data):
	import arxiv
	# https://github.com/lukasschwab/arxiv.py
	query = data["query"]
	maxResults = data["maxResults"] if "maxResults" in data else 5
	sortBy = arxiv.SortCriterion(data["sortBy"]) if "sortBy" in data else arxiv.SortCriterion.SubmittedDate
	sortOrder = arxiv.SortOrder(data["sortOrder"]) if "sortOrder" in data else arxiv.SortOrder.Descending
	client = arxiv.Client()
	search = arxiv.Search(
		query = query,
		max_results = maxResults,
		# https://info.arxiv.org/help/api/user-manual.html#3113-sort-order-for-return-results
		sort_by = sortBy,
		sort_order = sortOrder
	)
	results = client.results(search)
	# https://info.arxiv.org/help/api/user-manual.html#52-details-of-atom-results-returned
	return [{"summary": r.summary, "title": r.title} for r in results]

def search_arxiv_tool():
	from uncas_automation.assistant.assistant_tools import AssistantTool, AssistantToolParameter
	return AssistantTool(searchArxiv, "Search arXiv.org for articles on physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, electrical engineering and systems science, and economics", [
		AssistantToolParameter("query", "The query to search for"),
		AssistantToolParameter("maxResults", "The maximum number of results to return", type = "integer"),
		AssistantToolParameter("sortBy", "The field to sort by", enum = ["relevance", "lastUpdatedDate", "submittedDate"]),
		AssistantToolParameter("sortOrder", "The order to sort by", enum = ["ascending", "descending"])
	])

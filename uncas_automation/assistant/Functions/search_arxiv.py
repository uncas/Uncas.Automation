import arxiv
from arxiv import SortOrder, SortCriterion

def searchArxiv(query, maxResults = 5, 
				sortBy = SortCriterion.SubmittedDate, 
				sortOrder = SortOrder.Descending):
	# https://github.com/lukasschwab/arxiv.py
	client = arxiv.Client()
	search = arxiv.Search(
		query = query,
		max_results = maxResults,
		# https://info.arxiv.org/help/api/user-manual.html#3113-sort-order-for-return-results
		sort_by = arxiv.SortCriterion(sortBy),
		sort_order = arxiv.SortOrder(sortOrder)
	)
	results = client.results(search)
	# https://info.arxiv.org/help/api/user-manual.html#52-details-of-atom-results-returned
	return [{"summary": r.summary, "title": r.title} for r in results]

def search_arxiv_tool():
	from easai.assistant.tool import AssistantTool, AssistantToolParameter
	return AssistantTool(searchArxiv, "Search arXiv.org for articles on physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, electrical engineering and systems science, and economics", [
		AssistantToolParameter("query", "The query to search for"),
		AssistantToolParameter("maxResults", "The maximum number of results to return", type = "integer"),
		AssistantToolParameter("sortBy", "The field to sort by", enum = ["relevance", "lastUpdatedDate", "submittedDate"]),
		AssistantToolParameter("sortOrder", "The order to sort by", enum = ["ascending", "descending"])
	])

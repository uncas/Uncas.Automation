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

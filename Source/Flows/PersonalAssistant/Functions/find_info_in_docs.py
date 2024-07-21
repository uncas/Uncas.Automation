def getStore():
	from Flows.PersonalAssistant.EmbeddingVectorStore import EmbeddingVectorStore
	return EmbeddingVectorStore("Data/GoogleSheetList.db")

def syncDocs():
	# TODO: Read list of docs from sheet
	print("Syncing docs")
	store = getStore()
	import glob
	for file in glob.glob("Data/GoogleSheetList/TODO/*.txt"):
		print("Storing file ", file)
		store.save(file)

def findInfoInDocs(input):
	query = input["query"]
	# TODO: Check when docs were last synced
	# TODO: If sync was more than X days ago, then sync again
	store = getStore()
	docs = store.getSimilarities(query)
	result = "\n\n".join(doc.page_content for doc in docs)
	return result

def find_info_in_docs_tool():
	from Flows.PersonalAssistant.assistant_tools import AssistantTool, AssistantToolParameter
	return AssistantTool(findInfoInDocs, "Find info in work-related documentation", [
		AssistantToolParameter("query", "The thing to search for in the documentation")
	])
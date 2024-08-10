from uncas_automation.assistant.embedding_vector_store import EmbeddingVectorStore

def get_store() -> EmbeddingVectorStore:
	return EmbeddingVectorStore("Data/GoogleSheetList.db")

def sync_docs():
	# TODO: Read list of docs from sheet
	print("Syncing docs")
	store = get_store()
	import glob
	for file in glob.glob("Data/GoogleSheetList/TODO/*.txt"):
		print("Storing file ", file)
		store.save(file)

def find_info_in_docs(query):
	# TODO: Check when docs were last synced
	# TODO: If sync was more than X days ago, then sync again
	store = get_store()
	docs = store.get_similarities(query)
	result = "\n\n".join(doc.page_content for doc in docs)
	return result

def find_info_in_docs_tool():
	from easai.assistant.tool import AssistantTool, AssistantToolParameter
	return AssistantTool(find_info_in_docs, "Find info in work-related documentation", [
		AssistantToolParameter("query", "The thing to search for in the documentation")
	])
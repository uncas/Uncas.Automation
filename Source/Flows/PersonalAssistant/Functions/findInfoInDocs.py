def getStore():
	from Flows.PersonalAssistant.EmbeddingVectorStore import EmbeddingVectorStore
	store = EmbeddingVectorStore("Output/GoogleSheetList.db")

def syncDocs():
	# TODO: Read list of docs from sheet
	print("Syncing docs")
	store = getStore()
	import glob
	for file in glob.glob("Data/GoogleSheetList/1X9QhUocllUsrhW07g2X2O3CqBuURAFMXBqmjqkePvN8/*.txt"):
		print("Storing file ", file)
		store.save(file)

def findInfoInDocs(query):
	# TODO: Check when docs were last synced
	# TODO: If sync was more than X days ago, then sync again
	# Use RAG to extract information from docs
	store = getStore()
	#store.
	# return information
	pass
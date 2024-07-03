def syncDocs():
	from Flows.PersonalAssistant.EmbeddingVectorStore import EmbeddingVectorStore
	# Read list of docs from sheet
	# Read docs
	# Index docs
	print("Syncing docs")
	import glob
	store = EmbeddingVectorStore("Output/GoogleSheetList.db")
	for file in glob.glob("Data/GoogleSheetList/1X9QhUocllUsrhW07g2X2O3CqBuURAFMXBqmjqkePvN8/*.txt"):
		print("Storing file ", file)
		store.save(file)

def findInfoInDocs(query):
	# Check when docs were last synced
	# If sync was more than X days ago, then sync again
	# Use RAG to extract information from docs
	# return information
	pass
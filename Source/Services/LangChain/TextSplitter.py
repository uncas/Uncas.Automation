def splitText(text):
	from langchain_text_splitters import RecursiveCharacterTextSplitter
	text_splitter = RecursiveCharacterTextSplitter(
		# Set a really small chunk size, just to show.
		chunk_size=100,
		chunk_overlap=10,
		length_function=len,
		is_separator_regex=False,
	)
	texts = text_splitter.create_documents([text])
	print(texts)

def runSplitText():
	text = input("Text : ")
	splitText(text)
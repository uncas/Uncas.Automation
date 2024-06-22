def embed(text):
	from sentence_transformers import SentenceTransformer
	path = "../../public/all-MiniLM-L6-v2"
	model = SentenceTransformer(path)
	embeddings = model.encode(text)
	return embeddings

def runEmbed():
	text = input("Text : ")
	embeddings = embed(text)
	print(embeddings)

def getEmbedding(text):
	from openai import OpenAI
	client = OpenAI()
	return client.embeddings.create(
	  model="text-embedding-ada-002",
	  input=text,
	  encoding_format="float"
	)

def runGetEmbedding():
	text = input("Text : ")
	embedding = getEmbedding(text)
	print(embedding)
def getEmbedding(text):
	from openai import OpenAI
	from Utils.Settings import getSetting
	apiKey = getSetting("openAi")["apiKey"]
	client = OpenAI(api_key=apiKey)
	return client.embeddings.create(
	  model="text-embedding-ada-002",
	  input=text,
	  encoding_format="float"
	)

def runGetEmbedding():
	text = input("Text : ")
	embedding = getEmbedding(text)
	print(embedding)
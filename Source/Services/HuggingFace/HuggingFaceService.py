def getClient():
	from Utils.Settings import getSetting
	from huggingface_hub import InferenceClient
	huggingFaceToken = getSetting("huggingFace")["token"]
	return InferenceClient(token = huggingFaceToken)

def createImage(prompt):
	client = getClient()
	image = client.text_to_image(prompt)
	image.save("astronaut.png")

def runCreateImage():
	prompt = input("Prompt : ")
	createImage(prompt)

def generateText():
	prompt = input("Prompt : ")
	client = getClient()
	answer = client.text_generation(prompt, max_new_tokens = 100)
	print(answer)

def classifyText():
	prompt = input("Prompt : ")
	client = getClient()
	model = "cardiffnlp/twitter-roberta-base-sentiment-latest" # with positive, neutral, negative
	model = "SamLowe/roberta-base-go_emotions" # with many emotions
	answer = client.text_classification(prompt, model = model)
	print(answer)

def translate():
	prompt = input("Translate : ")
	client = getClient()
	model = "facebook/mbart-large-50-many-to-many-mmt"
	result = client.translation(prompt, model=model, src_lang="en_XX", tgt_lang="fr_XX")
	print(result)

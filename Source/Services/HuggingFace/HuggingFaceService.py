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
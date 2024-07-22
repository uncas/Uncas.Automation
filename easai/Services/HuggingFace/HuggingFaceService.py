def getClient():
	from easai.Utils.Settings import getSetting
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

def speak(text):
	client = getClient()
	audio = client.text_to_speech(text, model="espnet/kan-bayashi_ljspeech_vits")
	from pathlib import Path
	fileName = "Output/hello_world.flac"
	Path(fileName).write_bytes(audio)
	convertFlacToMp3(fileName)

def convertFlacToMp3(flacFileName):
	from subprocess import run
	mp3 = flacFileName.replace(".flac", ".mp3") 
	run(["~/Downloads/ffmpeg", "-i", flacFileName, "-c:v", "copy", "-b:a", "320k", mp3, "-y"])
	playMp3(mp3)

def playMp3(mp3FileName):
	import os
	os.system("open " + mp3FileName) 

def runSpeak():
	text = input("Text : ")
	speak(text)

def search():
	from huggingface_hub import HfApi, ModelFilter
	api = HfApi()
	models = api.list_models(task="image-classification")
	print(next(models))

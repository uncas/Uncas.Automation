def speak(text):
	from transformers import pipeline
	import scipy
	synthesiser = pipeline("text-to-speech", "suno/bark")
	speech = synthesiser(text, forward_params={"do_sample": True})
	scipy.io.wavfile.write("bark_out.wav")

def runSpeak():
	text = input("Text : ")
	speak(text)
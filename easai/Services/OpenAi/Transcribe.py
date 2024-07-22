def transcribe(inputAudioFileName, language = "da", responseFormat = "json"):
	from openai import OpenAI
	client = OpenAI()
	audioFile = open(inputAudioFileName, "rb")
	transcription = client.audio.transcriptions.create(
		model = "whisper-1",
		file = audioFile,
		language = language,
		response_format = responseFormat
	)
	audioFile.close()
	return transcription

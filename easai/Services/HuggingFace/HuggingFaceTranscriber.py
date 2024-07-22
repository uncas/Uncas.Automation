def transcribe(inputAudioFileName, language = "da"):
	from Utils.AudioUtils import sliceInto1MinuteChunks
	chunks = sliceInto1MinuteChunks(inputAudioFileName)
	from transformers import pipeline
	pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v2")
	kwargs = { "task" : "transcribe", "language" : "<|" + language + "|>"}
	transcriptions = []
	for chunk in chunks:
		transcription = pipe(chunk, generate_kwargs = kwargs)
		print(transcription)
		transcriptions.append(transcription)
	return "\n".join([transcription["text"] for transcription in transcriptions])
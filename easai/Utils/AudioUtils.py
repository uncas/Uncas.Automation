def convertToMp3(fileName):
	from subprocess import run
	mp3FileName = fileName + ".mp3"
	run(["ffmpeg", "-i", fileName, "-c:v", "copy", "-b:a", "320k", mp3FileName, "-y"])
	return mp3FileName

def sliceInto1MinuteChunks(inputAudioFileName):
	from pydub import AudioSegment
	sound = AudioSegment.from_mp3(inputAudioFileName)
	# len() and slicing are in milliseconds
	chunkLength = 60 * 1000
	fullLength = len(sound)
	if fullLength <= chunkLength:
		return [inputAudioFileName]

	# split into chunkLength chunks and return file names :
	overlap = 1000 * 2
	chunks = []
	numberOfChunks = (fullLength // chunkLength) + 1
	print(fullLength, numberOfChunks)
	for i in range(0, numberOfChunks):
		chunkStartIndex = i * chunkLength
		chunkEndIndex = chunkStartIndex + chunkLength + overlap
		print(i, chunkStartIndex, chunkEndIndex)
		chunks.append(inputAudioFileName + "-" + str(i) + ".mp3")
		chunk = sound[chunkStartIndex : chunkEndIndex]
		chunk.export(chunks[-1], format = "mp3")
	return chunks
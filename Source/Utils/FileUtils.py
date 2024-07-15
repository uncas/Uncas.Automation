def writeText(folder, file, text):
	writeOrAppendText(folder, file, text, "w")

def appendText(folder, file, text):
	writeOrAppendText(folder, file, text, "a")

def writeOrAppendText(folder, file, text, mode):
	from pathlib import Path
	Path(folder).mkdir(parents = True, exist_ok = True)
	f = open(folder + "/" + file, mode)
	f.write(text)
	f.close()

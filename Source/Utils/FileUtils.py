def write_text(folder : str, file : str, text : str):
	writeOrAppendText(folder, file, text, "w")

def appendText(folder, file, text):
	writeOrAppendText(folder, file, text, "a")

def writeOrAppendText(folder, file, text, mode):
	from pathlib import Path
	Path(folder).mkdir(parents = True, exist_ok = True)
	f = open(folder + "/" + file, mode)
	f.write(text)
	f.close()

def getFilePath(pathRelativeToSourceFolder):
	import os
	thisPath = os.path.realpath(__file__)
	sourcePath = os.path.join(os.path.dirname(thisPath), "..")
	return os.path.join(sourcePath, pathRelativeToSourceFolder)

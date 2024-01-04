def writeText(folder, file, text):
	from pathlib import Path
	Path(folder).mkdir(parents = True, exist_ok = True)
	f = open(folder + "/" + file, "w")
	f.write(text)
	f.close()
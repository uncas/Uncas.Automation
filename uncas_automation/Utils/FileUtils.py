def getFilePath(pathRelativeToSourceFolder):
	import os
	thisPath = os.path.realpath(__file__)
	sourcePath = os.path.join(os.path.dirname(thisPath), "..")
	return os.path.join(sourcePath, pathRelativeToSourceFolder)

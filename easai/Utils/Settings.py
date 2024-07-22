def getSetting(key, defaultValue = None):
	import json
	import os.path
	fileName = "Config/Settings.json"
	if not os.path.isfile(fileName):
		return defaultValue
	with open(fileName) as settingsFile:
		settings = json.load(settingsFile)
		return settings.get(key, defaultValue)

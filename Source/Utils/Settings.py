def getSetting(key):
	import json
	with open("Config/Settings.json") as settingsFile:
		settings = json.load(settingsFile)
		return settings[key]

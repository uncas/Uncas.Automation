def getSetting(key, defaultValue = None):
	from easai.utils.json_key_value_fetcher import fetch_json_key_value
	fileName = "Config/Settings.json"
	return fetch_json_key_value(fileName, key, defaultValue)

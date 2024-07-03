def getCurrentWeather(location):
	import random
	temp = random.randint(5, 19)
	if location["country"] == "Denmark":
		return {
			"temperature": str(temp),
			"unit": "C",
			"forecast": "rainy"
		}
	return {
		"temperature": str(temp+10),
		"unit": "C",
		"forecast": "sunny"
	}
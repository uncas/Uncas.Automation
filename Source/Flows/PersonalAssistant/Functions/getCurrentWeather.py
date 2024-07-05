# https://openweathermap.org/
# https://openweathermap.org/api/one-call-3
# https://github.com/csparpa/pyowm
# https://pyowm.readthedocs.io/en/latest/

# Welcome message when I signed up:
#   Thank you for subscribing to Free OpenWeatherMap!
#   API key:
#     Within the next couple of hours, your API key XXX will be activated and ready to use
#     You can later create more API keys on your account page: https://home.openweathermap.org/api_keys
#     Please, always use your API key in each API call
#   Endpoint:
#     Please, use the endpoint api.openweathermap.org for your API calls
#     Example of API call:
#     api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=API_KEY_HERE
#   Useful links:
#     API documentation https://openweathermap.org/api
#     Details of your plan https://openweathermap.org/price
#     Blog: https://openweather.co.uk/blog/category/weather
#     Support center & FAQ: https://openweathermap.force.com/
#   Contact us info@openweathermap.org.

def mapWeatherObjectToMyDesiredOutput(weather):
	# Mapping of: https://github.com/csparpa/pyowm/blob/master/pyowm/weatherapi25/weather.py
	wind = weather.wind()
	return {
		"time": weather.reference_time("iso"),
		"temperature": {
			"average": weather.temperature('celsius')["temp"],
			"unit": "Celsius"
		},
		"status": weather.detailed_status,
		"wind": {
			"speed": wind["speed"],
			"gust": wind["gust"],
			"direction": wind["deg"]
		},
		"rainProbability": weather.rain,
		"cloudCoveragePercentage": weather.clouds
	}

def getCurrentWeather(data):
	import os
	from pyowm import OWM

	countryCode = data["countryCode"] if "countryCode" in data else ""
	city = data["city"] if "city" in data else ""
	owm = OWM(os.getenv('OpenWeatherMap_Api_Key'))
	mgr = owm.weather_manager()
	place = city + ',' + countryCode
	observation = mgr.weather_at_place(place)
	weather = observation.weather

	# Forecast: https://pyowm.readthedocs.io/en/latest/v3/code-recipes.html#weather_forecasts
	forecast = list(mgr.forecast_at_place(place, '3h').forecast)
	
	return {
		"current": mapWeatherObjectToMyDesiredOutput(weather),
		"forecast": [mapWeatherObjectToMyDesiredOutput(item) for item in forecast[:8]]
	}
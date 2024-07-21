# From: https://pypi.org/project/googlemaps/
# Set up API key here: https://console.cloud.google.com/google/maps-apis/credentials
from datetime import datetime

class GoogleMapsService():
	def GetDirections(fromLocation : str, toLocation : str, mode : str = "driving", departureTime : datetime = None):
		import os
		import googlemaps
		from googlemaps.exceptions import ApiError

		gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
		departureTimeValue = datetime.now() if departureTime is None else departureTime
		try:
			directions_result = gmaps.directions(fromLocation, toLocation, mode = mode, departure_time = departureTimeValue)
			distanceKm = directions_result[0]['legs'][0]['distance']['value'] / 1000.0
			durationMinutes = directions_result[0]['legs'][0]['duration']['value'] / 60.0
			trafficDurationMinutes = directions_result[0]['legs'][0]['duration_in_traffic']['value'] / 60.0
			return {
				"distanceInKm": distanceKm,
				"durationInMinutes": durationMinutes,
				"trafficDurationInMinutes": trafficDurationMinutes
			}
		except ApiError as e:
			print(e)
			return {
				"error": "An error occurred. Consider using simpler or more general locations.",
				"errorDetails": str(e)
			}
# Example of what this service can do: https://www.themoviedb.org/movie/now-playing

# Docs: https://developer.themoviedb.org/docs/getting-started
# Forum: https://www.themoviedb.org/talk/category/5047958519c29526b50017d6
# Wrappers and libraries: https://developer.themoviedb.org/docs/wrappers-and-libraries
# Status: https://status.themoviedb.org/

# The python lib that I'm using: https://github.com/celiao/tmdbsimple/?tab=readme-ov-file

# API Keys: https://www.themoviedb.org/settings/api

import tmdbsimple as tmdb

class TmdbService:

	def __init__(self):
		import os
		tmdb.API_KEY = os.getenv('THEMOVIEDB_API_KEY')

	def getBestMatchingMovieId(self, movieTitle):
		search = tmdb.Search()
		response = search.movie(query=movieTitle)
		movieResponse = response["results"][0]
		return movieResponse["id"]

	def getWatchProvidersByMovieTitle(self, movieTitle):
		movieId = self.getBestMatchingMovieId(movieTitle)
		return self.getWatchProvidersByMovieId(movieId)

	def getWatchProvidersByMovieId(self, movieId):
		movie = tmdb.Movies(movieId)
		watchProviders = movie.watch_providers()["results"]
		myCountry = "DK"
		if not myCountry in watchProviders:
			return []

		providersInMyCountry = watchProviders[myCountry]
		myProviders = ["Viaplay", "HBO Max", "Netflix", "TV 2 Play"]
		types = ["rent", "buy", "flatrate", "ads"]
		options = []
		for type in types:
			if type in providersInMyCountry:
				for option in providersInMyCountry[type]:
					providerName = option["provider_name"]
					if providerName in myProviders and providerName not in options:
						options.append(providerName)
		return options

	def getRecommendedMoviesByMovieTitle(self, movieTitle):
		movieId = self.getBestMatchingMovieId(movieTitle)
		return self.getRecommendedMoviesByMovieId(movieId)

	def getRecommendedMoviesByMovieId(self, movieId):
		movie = tmdb.Movies(movieId)
		recommendations = movie.recommendations()
		return [{
			"title": recommendation["title"],
			"id": recommendation["id"],
			"rating": recommendation["vote_average"],
			"overview": recommendation["overview"]
		} for recommendation in recommendations["results"]]

# Example of what this service can do: https://www.themoviedb.org/movie/now-playing

# Docs: https://developer.themoviedb.org/docs/getting-started
# Forum: https://www.themoviedb.org/talk/category/5047958519c29526b50017d6
# Wrappers and libraries: https://developer.themoviedb.org/docs/wrappers-and-libraries
# Status: https://status.themoviedb.org/

# The python lib that I'm using: https://github.com/celiao/tmdbsimple/?tab=readme-ov-file

# API Keys: https://www.themoviedb.org/settings/api

import tmdbsimple as tmdb
import os
tmdb.API_KEY = os.getenv('THEMOVIEDB_API_KEY')

def getBestMatchingMovieId(movieTitle):
	search = tmdb.Search()
	response = search.movie(query=movieTitle)
	movieResponse = response["results"][0]
	return movieResponse["id"]

def getWatchProviders(movieInfo):
	movieTitle = movieInfo["movieTitle"]
	movieId = getBestMatchingMovieId(movieTitle)
	movie = tmdb.Movies(movieId)
	watchProviders = movie.watch_providers()
	myCountry = "DK"
	myProviders = ["Viaplay", "HBO Max", "Netflix", "TV 2 Play"]
	providersInMyCountry = watchProviders["results"][myCountry]
	types = ["rent", "buy", "flatrate", "ads"]
	options = []
	for type in types:
		if type in providersInMyCountry:
			for option in providersInMyCountry[type]:
				providerName = option["provider_name"]
				if providerName in myProviders and providerName not in options:
					options.append(providerName)
	return [{"providerName": option} for option in options]

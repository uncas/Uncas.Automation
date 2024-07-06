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
	return getWatchProvidersByMovieId(movieId)

def getWatchProvidersByMovieId(movieId):
	movie = tmdb.Movies(movieId)
	watchProviders = movie.watch_providers()["results"]
	myCountry = "DK"
	myProviders = ["Viaplay", "HBO Max", "Netflix", "TV 2 Play"]
	if not myCountry in watchProviders:
		return []

	providersInMyCountry = watchProviders[myCountry]
	types = ["rent", "buy", "flatrate", "ads"]
	options = []
	for type in types:
		if type in providersInMyCountry:
			for option in providersInMyCountry[type]:
				providerName = option["provider_name"]
				if providerName in myProviders and providerName not in options:
					options.append(providerName)
	return options

def getRecommendedMovies(movieId):
	movie = tmdb.Movies(movieId)
	recommendations = movie.recommendations()
	return [{
		"title": recommendation["title"],
		"id": recommendation["id"],
		"rating": recommendation["vote_average"],
		"overview": recommendation["overview"]
	} for recommendation in recommendations["results"]]

def getRecommendedMoviesThatIHaveAccessToWatch():
	favorites = getMyFavoriteMovies()
	recommendations = []
	moviesIHaveWatched = getMoviesIHaveWatched()
	for favorite in favorites:
		movieId = getBestMatchingMovieId(favorite)
		recommendedMovies = getRecommendedMovies(movieId)
		for movie in recommendedMovies:
			if movie["title"] not in moviesIHaveWatched:
				if movie not in recommendations:
					recommendations.append(movie)
	# Return list of recommended movies (sorted by rating)
	viable = []
	for movie in recommendations:
		watchProviders = getWatchProvidersByMovieId(movie["id"])
		if len(watchProviders) > 1:
			viable.append({
				"title": movie["title"],
				"id": movie["id"],
				"rating": movie["rating"],
				"providers": watchProviders})
	return sorted(viable, key=lambda d: d['rating'], reverse = True)

def getMyFavoriteMovies():
	return ["Ashes of time", "The Godfather"]

def getMoviesIHaveWatched():
	return ["The Godfather", "Ashes of time"]

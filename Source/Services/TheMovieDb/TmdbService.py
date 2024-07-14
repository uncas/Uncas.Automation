# Using The Movie Database:

# Example of what this service can do: https://www.themoviedb.org/movie/now-playing
# Docs: https://developer.themoviedb.org/docs/getting-started
# Forum: https://www.themoviedb.org/talk/category/5047958519c29526b50017d6
# Wrappers and libraries: https://developer.themoviedb.org/docs/wrappers-and-libraries
# Status: https://status.themoviedb.org/
# The python lib that I'm using: https://github.com/celiao/tmdbsimple/?tab=readme-ov-file
# API Keys: https://www.themoviedb.org/settings/api

import os
import tmdbsimple as tmdb
from Utils.LocalCache import LocalCache

class TmdbService:

	def __init__(self):
		tmdb.API_KEY = os.getenv('THEMOVIEDB_API_KEY')
		self.cache = LocalCache()

	def getBestMatchingMovieId(self, movieTitle):
		search = tmdb.Search()
		results = search.movie(query = movieTitle)["results"]
		return results[0]["id"] if len(results) > 0 else None

	def getWatchProvidersByMovieTitle(self, movieTitle):
		movieId = self.getBestMatchingMovieId(movieTitle)
		return self.getWatchProvidersByMovieId(movieId) if movieId else []

	def getWatchProvidersByMovieId(self, movieId):
		def _get():
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

		return self.cache.getOrAddWithLifetime("TheMovieDb_WatchProvidersByMovieId_" + str(movieId), _get, 3600 * 24 * 7)

	def getRecommendedMoviesByMovieTitle(self, movieTitle):
		movieId = self.getBestMatchingMovieId(movieTitle)
		return self.getRecommendedMoviesByMovieId(movieId) if movieId else []

	def getRecommendedMoviesByMovieId(self, movieId):
		movie = tmdb.Movies(movieId)
		recommendations = movie.recommendations()
		return [{
			"title": recommendation["title"],
			"id": recommendation["id"],
			"rating": recommendation["vote_average"],
			"overview": recommendation["overview"]
		} for recommendation in recommendations["results"]]

	def rateMovieByTitle(self, movieTitle, rating):
		movieId = self.getBestMatchingMovieId(movieTitle)
		self.rateMovieByMovieId(movieId, rating)

	def rateMovieByMovieId(self, movieId, rating):
		movie = tmdb.Movies(movieId)
		sessionId = self.getSessionId()
		movie.rating(session_id = sessionId, value = rating)

	def getSessionId(self):
		return self.cache.getOrAdd("TheMovieDb_SessionId", self.createSessionId)

	def createSessionId(self):
		import requests
		import webbrowser

		accessToken = os.getenv("THEMOVIEDB_ACCESS_TOKEN")
		headers = {
			"accept": "application/json",
			"content-type": "application/json",
			"Authorization": "Bearer " + accessToken
		}

		# Create request token:
		createRequestTokenUrl = "https://api.themoviedb.org/3/authentication/token/new"
		requestTokenResponse = requests.get(createRequestTokenUrl, headers = headers)
		requestToken = requestTokenResponse.json()["request_token"]
		
		# Ask user to confirm:
		forwardUrl = "https://www.themoviedb.org/authenticate/" + requestToken
		webbrowser.open(forwardUrl, new=0, autoraise=True)
		input("Press enter when you have confirmed in the browser...")
		
		# Create session:
		createSesssionUrl = "https://api.themoviedb.org/3/authentication/session/new"
		sessionResponse = requests.post(createSesssionUrl, json={ "request_token": requestToken }, headers=headers)
		return sessionResponse.json()["session_id"]
	
	def getMyFavoriteMovies(self):
		sessionId = self.getSessionId()
		account = tmdb.Account(sessionId)
		account.info()
		return account.favorite_movies()["results"]

	def getMoviesIHaveWatched(self):
		return self.getMoviesIHaveRated()

	def getMoviesIHaveRated(self):
		sessionId = self.getSessionId()
		account = tmdb.Account(sessionId)
		account.info()
		return account.rated_movies()["results"]

	def getMoviesPlayingNow(self):
		def _get():
			return tmdb.Movies().now_playing(region = "DK")["results"]
		return self.cache.getOrAddWithLifetime("TheMovieDb_MoviesNowPlaying", _get, 3600 * 24 * 3)

	def getPopularMovies(self):
		def _get():
			return tmdb.Movies().popular()["results"]
		return self.cache.getOrAddWithLifetime("TheMovieDb_PopularMovies", _get, 3600 * 24)

	def getTopRatedMovies(self, page = 1):
		def _get():
			return tmdb.Movies().top_rated(page = page)["results"]
		return self.cache.getOrAddWithLifetime("TheMovieDb_TopRatedMovies-page" + str(page), _get, 3600 * 24 * 3)

	def getTrendingMovies(self):
		def _get():
			return tmdb.Trending(media_type = "movie", time_window = "week").info()["results"]
		return self.cache.getOrAddWithLifetime("TheMovieDb_TrendingMovies", _get, 3600 * 24 * 7)
	
	def getGoodMoviesThatIHaveAccessToWatch(self, minRating = 5.0):
		movies = self.getTrendingMovies() + self.getMoviesPlayingNow() + self.getPopularMovies()
		for page in range(1, 5):
			movies += self.getTopRatedMovies(page)
		uniqueMovies = list({movie["id"]:movie for movie in movies}.values())
		sortedMovies = sorted(uniqueMovies, key = lambda movie: movie['vote_average'], reverse = True)
		for movie in sortedMovies:
			if movie["vote_average"] < minRating:
				continue
			watchProviders = self.getWatchProvidersByMovieId(movie["id"])
			if len(watchProviders) > 0:
				movie["watchProviders"] = watchProviders
				yield movie

def test_getMoviesPlayingNow():
	import json
	print(json.dumps(TmdbService().getMoviesPlayingNow())[:2000])

def test_getPopularMovies():
	import json
	print(json.dumps(TmdbService().getPopularMovies())[:2000])

def test_getTopRatedMovies():
	import json
	print(json.dumps(TmdbService().getTopRatedMovies())[:2000])
	print(json.dumps(TmdbService().getTopRatedMovies(2))[:2000])

def test_getTrendingMovies():
	import json
	print(json.dumps(TmdbService().getTrendingMovies())[:2000])

def test_getGoodMoviesThatIHaveAccessToWatch():
	for movie in TmdbService().getGoodMoviesThatIHaveAccessToWatch():
		print(movie["title"], movie["vote_average"], movie["watchProviders"])

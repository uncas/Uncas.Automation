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
from easai.utils.local_cache import LocalCache

class TmdbService:

	def __init__(self):
		tmdb.API_KEY = os.getenv('THEMOVIEDB_API_KEY')
		self.cache = LocalCache("Data/LocalCache.db")

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
			# Available types are:
			# buy: pay extra, 
			# rent: pay extra, 
			# flatrate: included in subscription, 
			# ads: with ads?
			types = ["flatrate", "ads"]
			options = []
			for type in types:
				if type in providersInMyCountry:
					for option in providersInMyCountry[type]:
						providerName = option["provider_name"]
						if providerName in myProviders and providerName not in options:
							options.append(providerName)
			return options

		return self.cache.get_or_add_with_lifetime("TheMovieDb_WatchProvidersByMovieId_" + str(movieId), _get, 3600 * 24 * 7)

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
		return self.cache.get_or_add("TheMovieDb_SessionId", self.createSessionId)

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
	
	def getMyFavoriteMovies(self, page = 1):
		def _get():
			sessionId = self.getSessionId()
			account = tmdb.Account(sessionId)
			account.info()
			return account.favorite_movies(page = page)["results"]
		return self.cache.get_or_add_with_lifetime("TheMovieDb_MyFavoriteMovies-page" + str(page), _get, 60 * 5)

	def getAllMoviesIHaveWatched(self):
		for page in range(1, 100):
			movies = self.getMoviesIHaveWatched(page)
			if len(movies) == 0:
				return
			for movie in movies:
				yield movie

	def getMoviesIHaveWatched(self, page = 1):
		return self.getMoviesIHaveRated(page)

	def getMoviesIHaveRated(self, page = 1):
		def _get():
			sessionId = self.getSessionId()
			account = tmdb.Account(sessionId)
			account.info()
			return account.rated_movies(page = page)["results"]
		return self.cache.get_or_add_with_lifetime("TheMovieDb_MoviesIHaveRated-page" + str(page), _get, 60 * 5)

	def getMoviesPlayingNow(self):
		def _get():
			return tmdb.Movies().now_playing(region = "DK")["results"]
		return self.cache.get_or_add_with_lifetime("TheMovieDb_MoviesNowPlaying", _get, 3600 * 24 * 3)

	def getPopularMovies(self):
		def _get():
			return tmdb.Movies().popular()["results"]
		return self.cache.get_or_add_with_lifetime("TheMovieDb_PopularMovies", _get, 3600 * 24)

	def getTopRatedMovies(self, page = 1):
		def _get():
			return tmdb.Movies().top_rated(page = page)["results"]
		return self.cache.get_or_add_with_lifetime("TheMovieDb_TopRatedMovies-page-" + str(page), _get, 3600 * 24 * 3)

	def getTrendingMovies(self):
		def _get():
			return tmdb.Trending(media_type = "movie", time_window = "week").info()["results"]
		return self.cache.get_or_add_with_lifetime("TheMovieDb_TrendingMovies", _get, 3600 * 24 * 7)
	
	def getWatchableMovies(self, minRating = 7, minVoteCount = 10):
		movies = self.getTrendingMovies() + self.getMoviesPlayingNow() + self.getPopularMovies()
		for page in range(1, 7):
			movies += self.getTopRatedMovies(page)
		uniqueMovies = list({movie["id"]:movie for movie in movies}.values())
		sortedMovies = sorted(uniqueMovies, key = lambda movie: movie['vote_average'], reverse = True)
		for movie in sortedMovies:
			if movie["vote_average"] < minRating or movie["vote_count"] < minVoteCount:
				continue
			watchProviders = self.getWatchProvidersByMovieId(movie["id"])
			if len(watchProviders) > 0:
				movie["watchProviders"] = watchProviders
				yield movie
	
	def getUnwatchedGoodWatchableMovies(self, minRating = 7, minVoteCount = 10):
		goodWatchableMovies = list(self.getWatchableMovies(minRating, minVoteCount))
		watchedMovies = list(self.getAllMoviesIHaveWatched())
		for goodWatchableMovie in goodWatchableMovies:
			if any(watchedMovie['id'] == goodWatchableMovie["id"] for watchedMovie in watchedMovies):
				continue
			yield self.withGenres(goodWatchableMovie)
	
	def withGenres(self, movie):
		genres = self.getGenres()
		movie["genres"] = [genre["name"] for genre in genres if genre["id"] in movie["genre_ids"]]
		return movie

	def getGenres(self):
		def _get():
			return tmdb.Genres().movie_list()
		return self.cache.get_or_add_with_lifetime("TheMovieDb_Genres", _get, 3600 * 24 * 7)["genres"]

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
	movies = list(TmdbService().getWatchableMovies())
	for movie in movies:
		print(movie["title"], movie["vote_average"], movie["watchProviders"])
	print(movies[0])

def test_getMyFavoriteMovies():
	movies = TmdbService().getMyFavoriteMovies()
	for movie in movies:
		print(movie["title"])

def test_getMoviesIHaveWatched():
	movies = TmdbService().getMoviesIHaveWatched(1)
	for movie in movies:
		print(movie["title"])

def test_getAllMoviesIHaveWatched():
	movies = TmdbService().getAllMoviesIHaveWatched()
	for movie in movies:
		print(movie["title"])

def test_getUnwatchedGoodWatchableMovies():
	movies = TmdbService().getUnwatchedGoodWatchableMovies()
	for movie in movies:
		print(movie["title"], "(", movie["genres"], movie["release_date"], ")", movie["vote_average"], movie["vote_count"], movie["watchProviders"])

def test_getGenres():
	genres = TmdbService().getGenres()
	for genre in genres:
		print(genre)
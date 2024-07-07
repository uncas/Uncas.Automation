from Services.TheMovieDb.TmdbService import TmdbService

def getWatchProviders(movieInfo):
	tmdbService = TmdbService()
	movieTitle = movieInfo["movieTitle"]
	return tmdbService.getWatchProvidersByMovieTitle(movieTitle)

def getRecommendedMoviesThatIHaveAccessToWatch():
	tmdbService = TmdbService()
	favorites = getMyFavoriteMovies()
	recommendations = []
	moviesIHaveWatched = getMoviesIHaveWatched()
	for favorite in favorites:
		recommendedMovies = tmdbService.getRecommendedMoviesByMovieTitle(favorite)
		for movie in recommendedMovies:
			if movie["title"] not in moviesIHaveWatched:
				if movie not in recommendations:
					recommendations.append(movie)
	viable = []
	for movie in recommendations:
		watchProviders = tmdbService.getWatchProvidersByMovieId(movie["id"])
		if len(watchProviders) > 1:
			viable.append({
				"title": movie["title"],
				"id": movie["id"],
				"rating": movie["rating"],
				"providers": watchProviders})
	return sorted(viable, key = lambda d: d['rating'], reverse = True)

def getMyFavoriteMovies():
	return ["Ashes of time", "The Godfather"]

def getMoviesIHaveWatched():
	return ["The Godfather", "Ashes of time"]

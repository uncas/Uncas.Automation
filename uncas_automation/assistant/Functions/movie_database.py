from uncas_automation.Services.TheMovieDb.TmdbService import TmdbService

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

def getUnwatchedGoodWatchableMovies():
	tmdb = TmdbService()
	return list(tmdb.getUnwatchedGoodWatchableMovies())

def get_unwatched_good_watchable_movies_tool():
	from uncas_automation.assistant.assistant_tools import AssistantTool
	return AssistantTool(getUnwatchedGoodWatchableMovies, "Get unwatched good watchable movies")

def get_watch_providers_tool():
	from uncas_automation.assistant.assistant_tools import AssistantTool, AssistantToolParameter
	return AssistantTool(getWatchProviders, "Gets watch providers for a given movie", [
		AssistantToolParameter("movieTitle", "The title of the movie")
	])
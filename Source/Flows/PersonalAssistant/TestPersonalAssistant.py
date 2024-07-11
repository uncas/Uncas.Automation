def testIt():
	#from Flows.PersonalAssistant.Functions.findInfoInDocs import syncDocs # type: ignore
	#syncDocs()

	#from Flows.PersonalAssistant.Functions.findInfoInDocs import findInfoInDocs # type: ignore
	#info = findInfoInDocs("What are the plans for the office space?")
	#print(info)

	#from Flows.PersonalAssistant.Functions.getLatestNews import getNewsDetails, getLatestNews
	#news = getLatestNews()
	#print(news)
	#print(getNewsDetails(news[0]))

	#from Flows.PersonalAssistant.Functions.searchArxiv import searchArxiv
	#papers = searchArxiv({"query": "rag"})
	#print(papers)

	#from Flows.PersonalAssistant.Functions.getCurrentWeather import getCurrentWeather
	#weather = getCurrentWeather({"city": "Copenhagen", "countryCode": "DK"})
	#print("Weather: ", weather)

	#from Flows.PersonalAssistant.Functions.theMovieDb import getRecommendedMoviesThatIHaveAccessToWatch
	#movies = getRecommendedMoviesThatIHaveAccessToWatch()
	#for movie in movies:
	#	print(movie["rating"], movie["title"], movie["providers"])

	#from Services.TheMovieDb.TmdbService import TmdbService
	#tmdbService = TmdbService()
	#tmdbService.rateMovieByTitle("Ashes of Time", 10)
	#tmdbService.rateMovieByTitle("The Godfather", 9)
	#print(tmdbService.getMyFavoriteMovies())
	#print(tmdbService.getMoviesIHaveWatched())

	#from Flows.PersonalAssistant.Functions.generateImage import generateImage, makePartOfImageTransparent
	#image = generateImage("A steampunk city with gear-driven machines, airships docked atop buildings, and streets lit by gas lamps, set in a vast canyon")
	#print(image)

	#from pathlib import Path
	#downloadsPath = str(Path.home() / "Downloads")
	#originalFilePath = downloadsPath + "/skriget.jpg"
	#newFilePath = downloadsPath + "/skriget_transparent.png"
	#xFraction, yFraction, widthFraction, heightFraction = 0.1, 0.1, 0.5, 0.5
	#makePartOfImageTransparent(originalFilePath, newFilePath, xFraction, yFraction, widthFraction, heightFraction)

	#from Flows.PersonalAssistant.Functions.createAssistant import createAndRunAssistant
	#createAndRunAssistant()

	#from Flows.PersonalAssistant.Functions.createJiraIssue import getMyJiraIssues, createJiraIssue
	#print(getMyJiraIssues()[0])
	#print(createJiraIssue({"summary": "TEST SUMMARY", "description": "TEST DESCRIPTION"}))

	from Flows.PersonalAssistant.Functions.getCalendarEvents import getCalendarEvents
	for item in getCalendarEvents():
		print(item) 

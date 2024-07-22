def testIt():
	#from easai.Flows.PersonalAssistant.Functions.findInfoInDocs import syncDocs # type: ignore
	#syncDocs()

	#from easai.Flows.PersonalAssistant.Functions.findInfoInDocs import findInfoInDocs # type: ignore
	#info = findInfoInDocs("What are the plans for the office space?")
	#print(info)

	#from easai.Flows.PersonalAssistant.Functions.getLatestNews import getNewsDetails, getLatestNews
	#news = getLatestNews()
	#print(news)
	#print(getNewsDetails(news[0]))

	#from easai.Flows.PersonalAssistant.Functions.searchArxiv import searchArxiv
	#papers = searchArxiv({"query": "rag"})
	#print(papers)

	#from easai.Flows.PersonalAssistant.Functions.getCurrentWeather import getCurrentWeather
	#weather = getCurrentWeather({"city": "Copenhagen", "countryCode": "DK"})
	#print("Weather: ", weather)

	#from easai.Flows.PersonalAssistant.Functions.theMovieDb import getRecommendedMoviesThatIHaveAccessToWatch
	#movies = getRecommendedMoviesThatIHaveAccessToWatch()
	#for movie in movies:
	#	print(movie["rating"], movie["title"], movie["providers"])

	#from easai.Services.TheMovieDb.TmdbService import TmdbService
	#tmdbService = TmdbService()
	#tmdbService.rateMovieByTitle("Ashes of Time", 10)
	#tmdbService.rateMovieByTitle("The Godfather", 9)
	#print(tmdbService.getMyFavoriteMovies())
	#print(tmdbService.getMoviesIHaveWatched())

	#from easai.Flows.PersonalAssistant.Functions.generateImage import generateImage, makePartOfImageTransparent
	#image = generateImage("A steampunk city with gear-driven machines, airships docked atop buildings, and streets lit by gas lamps, set in a vast canyon")
	#print(image)

	#from pathlib import Path
	#downloadsPath = str(Path.home() / "Downloads")
	#originalFilePath = downloadsPath + "/skriget.jpg"
	#newFilePath = downloadsPath + "/skriget_transparent.png"
	#xFraction, yFraction, widthFraction, heightFraction = 0.1, 0.1, 0.5, 0.5
	#makePartOfImageTransparent(originalFilePath, newFilePath, xFraction, yFraction, widthFraction, heightFraction)

	#from easai.Flows.PersonalAssistant.Functions.createAssistant import createAndRunAssistant
	#createAndRunAssistant()

	#from easai.Flows.PersonalAssistant.Functions.createJiraIssue import getMyJiraIssues, createJiraIssue
	#print(getMyJiraIssues()[0])
	#print(createJiraIssue({"summary": "TEST SUMMARY", "description": "TEST DESCRIPTION"}))

	#from easai.Flows.PersonalAssistant.Functions.getCalendarEvents import getCalendarEvents
	#for item in getCalendarEvents():
	#	print(item) 

	#from easai.Flows.PersonalAssistant.Functions.readWebPage import readWebPage
	#print(readWebPage("https://github.com/uncas/Uncas.Automation/blob/main/easai/Flows/PersonalAssistant/Readme.md"))
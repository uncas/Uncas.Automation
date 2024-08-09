from dotenv import load_dotenv
load_dotenv(override = True)

#from uncas_automation.Services.Movies.CinemaService import test_getMovies, test_getMoviesOnDate
#test_getMovies()
#test_getMoviesOnDate()

#from uncas_automation.Utils.LocalCache import test_getOrAddWithLifetime, test_getOrAdd
#test_getOrAdd()
#test_getOrAddWithLifetime()

#from uncas_automation.Services.TheMovieDb.TmdbService import test_getTrendingMovies, test_getGoodMoviesThatIHaveAccessToWatch, test_getPopularMovies, test_getMoviesPlayingNow, test_getTopRatedMovies
#from uncas_automation.Services.TheMovieDb.TmdbService import test_getMoviesIHaveWatched, test_getMyFavoriteMovies, test_getAllMoviesIHaveWatched, test_getUnwatchedGoodWatchableMovies, test_getGenres
#test_getTrendingMovies()
#test_getGoodMoviesThatIHaveAccessToWatch()
#test_getPopularMovies()
#test_getMoviesPlayingNow()
#test_getTopRatedMovies()
#test_getMoviesIHaveWatched()
#test_getMyFavoriteMovies()
#test_getAllMoviesIHaveWatched()
#test_getUnwatchedGoodWatchableMovies()
#test_getGenres()

#from uncas_automation.Services.Google.GoogleCalendarService import test_getCalendarEvents
#test_getCalendarEvents()

#from uncas_automation.Services.HuggingFace.HuggingFaceTranscriber import transcribe
#from uncas_automation.Utils.AudioUtils import convertToMp3
#fileName = "../../../Downloads/test.m4a"
#mp3FileName = convertToMp3(fileName)
#textFileName ="transcription-test.txt"
#transcription = transcribe(mp3FileName)
#print(transcription)
#from uncas_automation.Utils.FileUtils import writeText
#writeText("Output", textFileName, transcription)

#from uncas_automation.Services.Google.GoogleDriveServiceTests import test_exportDocumentAsMarkdown
#test_exportDocumentAsMarkdown()

from tests.test_GoogleDocsService_integration import test_readDocument
test_readDocument()
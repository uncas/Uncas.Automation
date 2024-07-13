def getMovies():
	cinemas = [
		{"name": "Vue Bruuns", "url": "https://kino.dk/biografer/Vue-Bruuns"},
		{"name": "Øst for Paradis", "url": "https://kino.dk/biografer/oest-paradis"},
		{"name": "Nordisk Film Biografer Aarhus C", "url": "https://kino.dk/biografer/nordisk-film-biografer-aarhus-c"},
		{"name": "Nordisk Film Biografer Troejborg", "url": "https://kino.dk/biografer/nordisk-film-biografer-troejborg"},
	]
	for cinema in cinemas:
		for movie in getMoviesInCinema(cinema):
			yield movie

def getMoviesInCinema(cinema):
	import json
	from Utils.LocalCache import getOrAddWithLifetime
	key = "getMoviesInCinema: " + cinema["name"]
	lifetimeSeconds = 3600 * 3
	return json.loads(getOrAddWithLifetime(key, lambda: json.dumps(getMoviesInCinema_NonCached(cinema)), lifetimeSeconds))

def getMoviesInCinema_NonCached(cinema):
	import urllib.request
	import certifi
	import re
	userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
	req = urllib.request.Request(cinema["url"])
	req.add_header('User-Agent', userAgent)
	r = urllib.request.urlopen(req, cafile=certifi.where())
	html = r.read()
	from bs4 import BeautifulSoup 
	soup = BeautifulSoup(html, "html.parser")
	movieDivs = soup.find_all("div", {"class": "movie-showtimes__movie-item"})
	movies = []
	regex = r"(\d*)\/(\d*)"
	for movieDiv in movieDivs:
		desktop = movieDiv.find("div", {"class": "movie-showtimes__metadata-desktop"})
		title = desktop.find("h2").text
		dayDivs = movieDiv.find_all("div", {"class": "swiper-slide date-picker__weekday-item"})
		dates = []
		for dayDiv in dayDivs:
			dateText = dayDiv.find("div", {"class": "date-picker__weekday-name"}).text
			match = re.search(regex, dateText)
			day = match.group(1)
			month = match.group(2)
			timesDiv = dayDiv.find_all("div", {"class": "date-picker__time"})
			times = [timeDiv.text for timeDiv in timesDiv]
			date = {"day": day, "month": month, "times": times}
			dates.append(date)
		movies.append({ "title" : title, "cinema" : cinema["name"], "dates" : dates })
	return movies

def test_getMovies():
	import json
	for movie in getMovies():
		print(movie["title"], movie["cinema"], json.dumps(movie["dates"]))
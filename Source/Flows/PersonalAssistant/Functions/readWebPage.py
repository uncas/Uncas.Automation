def readWebPage(data):
	url = data["url"]
	import bs4, requests
	response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
	soup = bs4.BeautifulSoup(response.text, 'html.parser')
	return soup.body.get_text(' ', strip = True)
def get_electric_cars_in_denmark():
	url = "https://blog.bilbasen.dk/elbiler-i-danmark-2021-353560/"
	import urllib.request
	import certifi
	userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
	req = urllib.request.Request(url)
	req.add_header('User-Agent', userAgent)
	cafile= certifi.where()
	r = urllib.request.urlopen(req, cafile=cafile)
	html = r.read()
	from bs4 import BeautifulSoup 
	soup = BeautifulSoup(html, "html.parser")
	return soup.get_text()

def read_web_page_text(url):
	import bs4
	soup = bs4.BeautifulSoup(read_web_page_html(url), 'html.parser')
	return soup.get_text(' ', strip = True)

def read_web_page_html(url):
	import requests
	response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'})
	if response.status_code != 200:
		print("Error: ", response.status_code, response.headers)
	return response.text

def read_web_page_markdown(url):
	import html2text
	textMaker = html2text.HTML2Text()
	return textMaker.handle(read_web_page_html(url))	

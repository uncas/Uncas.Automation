def read_web_page_text(url):
	import bs4
	soup = bs4.BeautifulSoup(read_web_page_html(url), 'html.parser')
	return soup.body.get_text(' ', strip = True)

def read_web_page_html(url):
	import requests
	response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
	return response.text

def read_web_page_markdown(url):
	import html2text
	textMaker = html2text.HTML2Text()
	return textMaker.handle(read_web_page_html(url))	

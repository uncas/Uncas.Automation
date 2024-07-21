def getLatestNews():
	from rss_parser import RSSParser
	from requests import get

	rss_url = "https://www.dr.dk/nyheder/service/feeds/allenyheder"
	response = get(rss_url)
	rss = RSSParser.parse(response.text)
	return [{"title": item.title.content, "newsLink": item.link.content} for item in rss.channel.items]

def getNewsDetails(input):
	from requests import get
	from bs4 import BeautifulSoup 

	newsLink = input["newsLink"]
	response = get(newsLink)
	html = response.text

	# Get text content of elements like this:
	# <div class="hydra-latest-news-page-short-news-article__body" itemprop="articleBody">

	cssClass = "hydra-latest-news-page-short-news-article__body"
	itemprop = "articleBody"

	soup = BeautifulSoup(html, 'html.parser')
	article = soup.find('div', class_ = cssClass)
	content = article.find('div', itemprop = itemprop)
	text = content.get_text()
	return text

def getLatestNewsTool():
	from Flows.PersonalAssistant.AssistantTools import AssistantTool
	return AssistantTool(getLatestNews, "Get the latest news")

def getNewsDetailsTool():
	from Flows.PersonalAssistant.AssistantTools import AssistantTool, AssistantToolParameter
	return AssistantTool(getNewsDetails, "Get details about news in the provided link", [
		AssistantToolParameter("newsLink", "The link to the news")
	])
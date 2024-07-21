def get_latest_news():
	from rss_parser import RSSParser
	from requests import get

	rss_url = "https://www.dr.dk/nyheder/service/feeds/allenyheder"
	response = get(rss_url)
	rss = RSSParser.parse(response.text)
	return [{"title": item.title.content, "news_link": item.link.content} for item in rss.channel.items]

def get_news_details(input):
	from requests import get
	from bs4 import BeautifulSoup 

	news_link = input["news_link"]
	response = get(news_link)
	html = response.text

	# Get text content of elements like this:
	# <div class="hydra-latest-news-page-short-news-article__body" itemprop="articleBody">

	css_class = "hydra-latest-news-page-short-news-article__body"
	itemprop = "articleBody"

	soup = BeautifulSoup(html, 'html.parser')
	article = soup.find('div', class_ = css_class)
	content = article.find('div', itemprop = itemprop)
	text = content.get_text()
	return text

def get_latest_news_tool():
	from Flows.PersonalAssistant.assistant_tools import AssistantTool
	return AssistantTool(get_latest_news, "Get the latest news")

def get_news_details_tool():
	from Flows.PersonalAssistant.assistant_tools import AssistantTool, AssistantToolParameter
	return AssistantTool(get_news_details, "Get details about news in the provided link", [
		AssistantToolParameter("news_link", "The link to the news")
	])
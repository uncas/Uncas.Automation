def getLatestNews():
	from rss_parser import RSSParser
	from requests import get

	rss_url = "https://www.dr.dk/nyheder/service/feeds/allenyheder"
	response = get(rss_url)
	rss = RSSParser.parse(response.text)
	return "\n".join([item.title.content for item in rss.channel.items])
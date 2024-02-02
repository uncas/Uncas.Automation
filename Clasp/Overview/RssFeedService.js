function debug_readRssFeed() {
	var url = "https://feeds.feedburner.com/blogspot/gJZg";
	var rss = readRssFeed(url);
	Logger.log(Array.from(rss));
}
  
function* readRssFeed(feed) {
	var content = UrlFetchApp.fetch(feed).getContentText();
	var doc = Xml.parse(content, false);  
	const channelTitle = doc.getElement().getElement("channel").getElement("title").getText();
	Logger.log(channelTitle);
	var items = doc.getElement().getElement("channel").getElements("item");   
	for (var i in items) {
		const item  = items[i];
		const title = item.getElement("title").getText();
		const link  = item.getElement("link").getText();
		const date  = item.getElement("pubDate").getText();
		const desc  = item.getElement("description").getText();
		yield { title: title, link: link, date: date, desc: desc };
	}
}

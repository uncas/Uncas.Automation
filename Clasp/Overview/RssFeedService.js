function debug_readRssFeed() {
	const url = "https://feeds.feedburner.com/blogspot/gJZg";
	const entries = readRssFeed(url);
	entries.forEach(entry => {
		Logger.log(entry.title);
		Logger.log(entry.link);
		Logger.log(entry.id);
		Logger.log(entry.published);
		Logger.log(entry.content.substring(0, 1000));
	});
}

function readRssFeed(feed) {
	const content = UrlFetchApp.fetch(feed).getContentText();
	const doc = XmlService.parse(content);
	const children = doc.getRootElement().getChildren();
	const entries = children.filter(c => c.getName() == "entry");
	return entries.map(entry => {
		const values = getEntryValues(entry);
		const title = values.filter(v => v.name == "title")[0].text;
		const id = values.filter(v => v.name == "id")[0].text;
		const published = values.filter(v => v.name == "published")[0].text;
		const content = values.filter(v => v.name == "content")[0].text;
		// TODO: Include categories!
		const link = values.filter(v => v.name == "link" && v.rel =="alternate")[0].href;
		return {title: title, content: content, link: link, id: id, published: published};
	});
}

function getEntryValues(entry) {
	return entry.getChildren().map(attribute => {
		const name = attribute.getName();
		const text = attribute.getText();
		let rel = null, href = null;
		if (name == "link") {
			const linkAttributes = attribute.getAttributes();
			rel = linkAttributes.filter(x => x.getName() == "rel")[0].getValue();
			href = linkAttributes.filter(x => x.getName() == "href")[0].getValue();
		}
		return {name: name, text: text, rel: rel, href: href};
	});
}
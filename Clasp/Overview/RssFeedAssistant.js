function debug_assistWithRssFeeds() {
	// A typical article: 4k tokens input, 1.5 k tokens output
	// Price with chat gpt 3.5: 0.005 $ per article
	// 200 articles per $ ! That is cheap!
	// https://huggingface.co/blog/feed.xml
	const url = "https://feeds.feedburner.com/blogspot/gJZg";
	const entries = readRssFeed(url);
	const entry = entries[0];
	const text = getPlainTextFromHtml(entry.content);
	const question = "Extract a list of techniques, tools, or technologies from the following article. " +
		"The response should only contain pure json with this structure: " +
		"{ items: [ {name, category, description, link} ]} " +
		"Category should indicate the category tree of the item, and be formatted as category/sub-category/sub-sub-category. " +
		"Description should be maximum 40 words, assume no prior specialized knowledge, and may be enriched with knowledge beyond the article. " +
		"Link should be to any relevant link found in the article. " +
		"Here is the article: " + 
		text;
	const answer = askChatGpt(question);
	Logger.log(answer);
}

function getPlainTextFromHtml(html) {
	const temp = GmailApp.createDraft("", "", "", { htmlBody: html });
	const plainText = temp.getMessage().getPlainBody();
	temp.deleteDraft();
	return plainText;
  }
  
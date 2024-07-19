function summarizeAndSlackSummary() {
	const summary = getSummaryFromChatGpt();
	slackSummary(summary)
}

function getSummaryFromChatGpt() {
	const journal = extractSingleTextFromGoogleDoc()
	const prompt = "Please summarize the following journal: " + journal;
	const answer = askChatGpt(prompt)
	return answer;
}

function extractSingleTextFromGoogleDoc() {
	const doc = DocumentApp.getActiveDocument();
	const body = doc.getBody();
	const text = body.getText();
	return text
}

function getDatedEntriesFromLastNDays(numberOfDays) {
	const datedEntries = getDatedEntries();
	const lastNDays = datedEntries.filter(entry => entry.date > new Date() - numberOfDays * 24 * 60 * 60 * 1000);
	lastNDays.forEach(function(entry) {
		Logger.log(entry)
	})
	return lastNDays;
}

function getDatedEntries() {
	const paragraphs = extractParagraphsFromGoogleDoc();
	const datedEntries = [];
	var entry = null;
	paragraphs.forEach(function(paragraph) {
		if (paragraph.heading === DocumentApp.ParagraphHeading.HEADING1) {
			// Skip this one
		}
		else if (paragraph.heading === DocumentApp.ParagraphHeading.HEADING2) {
			const dateString = paragraph.text.slice(0, 10);
			const date = new Date(dateString);
			entry = {date: date, texts: [paragraph.text]};
			datedEntries.push(entry);
		}
		else {
			entry.texts.push(paragraph.text);
		}
	});
	return datedEntries;
}

function extractParagraphsFromGoogleDoc() {
	const doc = DocumentApp.getActiveDocument()
	const body = doc.getBody();
	const paragraphs = body.getParagraphs();
	const paragraphObjects = [];
	paragraphs.forEach(function(paragraph) {
		const text = paragraph.getText();
		paragraphObjects.push({ text: text, heading: paragraph.getHeading() });
	});
	return paragraphObjects;
}


function slackSummary(summary) {
	const scriptProperties = PropertiesService.getScriptProperties();
	const url = scriptProperties.getProperty("Slack.WebhookUrl");
	const headers = {
		"Content-Type": "application/json"
	};
	const payload = {
		"summary": summary
	}
	const options = {
		"method": "post",
		"headers": headers,
		"payload": JSON.stringify(payload)
	};
	UrlFetchApp.fetch(url, options);
}

// Pricing: https://openai.com/api/pricing/
function askChatGpt(question) {
	const scriptProperties = PropertiesService.getScriptProperties();
	const apiKey = scriptProperties.getProperty("ChatGpt.ApiKey");
	const url = "https://api.openai.com/v1/chat/completions";
	const headers = {
		"Content-Type": "application/json",
		"Authorization": "Bearer " + apiKey
	};
	const payload = {
		"model": "gpt-4o-mini",
		"messages": [{"role": "user", "content": question}]
	};
	const options = {
		"method": "post",
		"headers": headers,
		"payload": JSON.stringify(payload)
	};
	const response = UrlFetchApp.fetch(url, options);
	const jsonResponse = JSON.parse(response);
	return jsonResponse.choices[0].message.content;
}
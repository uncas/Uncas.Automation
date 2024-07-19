function summarizeAndSlackSummary() {
	const summary = getSummaryFromChatGpt();
	slackSummary(summary);
}

function getSummaryFromChatGpt() {
	const journal = getTextFromLastNDays(6);
	if (journal === null) {
		return "No journal entries from the last 6 days.";
	}
	const userPrompt = "Please summarize the following journal entries: " + journal;
	const systemPrompt = getSystemPrompt();
	const answer = askChatGpt(userPrompt, systemPrompt);
	return answer;
}

function extractSingleTextFromGoogleDoc() {
	const doc = DocumentApp.getActiveDocument();
	const body = doc.getBody();
	const text = body.getText();
	return text
}

function getTextFromLastNDays(numberOfDays = 6) {
	const entries = getDatedEntriesFromLastNDays(numberOfDays);
	if (entries.length === 0) {
		return null;
	}
	const text = entries.map(entry => entry.texts.join("\n")).join("\n\n");
	return text;
}

function getDatedEntriesFromLastNDays(numberOfDays) {
	const datedEntries = getDatedEntries();
	const lastNDays = datedEntries.filter(entry => entry.date > new Date() - numberOfDays * 24 * 60 * 60 * 1000);
	//lastNDays.forEach(function(entry) {
	//	Logger.log(entry)
	//})
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
function askChatGpt(userPrompt, systemPrompt = null) {
	const scriptProperties = PropertiesService.getScriptProperties();
	const apiKey = scriptProperties.getProperty("ChatGpt.ApiKey");
	const url = "https://api.openai.com/v1/chat/completions";
	const headers = {
		"Content-Type": "application/json",
		"Authorization": "Bearer " + apiKey
	};
	const messages = [];
	if (systemPrompt) {
		messages.push({ role: "system", content: systemPrompt });
	}
	messages.push({ role: "user", content: userPrompt });
	const payload = {
		"model": "gpt-4o-mini",
		"messages": messages
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

function getSystemPrompt() {
	return "\
# IDENTITY and PURPOSE\
You are an expert journal summarizer. You take content in and output a summary formatted for slacking in the team's slack channel.\
Take a deep breath and think step by step about how to best accomplish this goal using the following steps.\
\
# OUTPUT SECTIONS\
- Combine all of your understanding of the content into a single, 20-word sentence in a section called SHORT SUMMARY.\
- Output the 10 most important points of the content as a list with no more than 15 words per point into a section called MAIN POINTS.\
- Output a list of any actions that appear important from the content in a section called ACTION POINTS.\
\
# OUTPUT INSTRUCTIONS\
- Create the output using the formatting above.\
- You only output human readable content suitable for a slack message.\
- Output bullets.\
- Do not output warnings or notes—just the requested sections.\
- Do not repeat items in the output sections.\
- Do not start items with the same opening words.\
\
# INPUT:\
INPUT:";
}
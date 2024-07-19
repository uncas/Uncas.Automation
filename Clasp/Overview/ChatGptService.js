function debug_askChatGptAboutEmail() {
	const answer = askChatGptAboutEmail(
		"Big opportunity!",
		"Hi! I have an opportunity for you! Can you meet next Wednesday? Best regards, Holger",
		"test@gmail.com");
	Logger.log(answer);
}

// TODO: Remove sensistive parts from body...
function askChatGptAboutEmail(subject, body, sender) {
	const question = "Jeg har modtaget nedenstående email; kan du foreslå en handling til mig på baggrund af emailen? Antag at beskeden ikke er et forsøg på svindel. Afsender: "
    + sender + ". Emne: " + subject + ". Indhold: " + body;
	return askChatGpt(question);
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
	Logger.log(jsonResponse);
	return jsonResponse.choices[0].message.content;
}
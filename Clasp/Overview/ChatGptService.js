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

/* Cost:
 GPT 3.5: 	$0.0015 / 1K input tokens	$0.0020 / 1K output tokens
 GPT 4: $0.03 / 1K input tokens	$0.06 / 1K output tokens
 Typical mail:
	500 tokens input: 3.5 cost: $0.00075, 4 cost: $0.015
	200 tokens output: 3.5 cost: $0.0004, 4 cost: $0.012
	Total cost for 1 mail: 3.5 cost: $0.00115 (0.008 DKK), 4 cost: $0.027 (0.18 DKK)
	Mails per DKK: GPT 3.5: 25 mails/DKK. GPT 4: 5 mails/DKK
*/
function askChatGpt(question) {
	const scriptProperties = PropertiesService.getScriptProperties();
	const apiKey = scriptProperties.getProperty("ChatGpt.ApiKey");
	const url = "https://api.openai.com/v1/chat/completions";
	const headers = {
		"Content-Type": "application/json",
		"Authorization": "Bearer " + apiKey
	};
	const payload = {
		"model": "gpt-3.5-turbo",
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
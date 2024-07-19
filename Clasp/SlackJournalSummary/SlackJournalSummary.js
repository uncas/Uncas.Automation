function summarizeAndSlackSummary()  {
	summary = getSummaryFromChatGpt();
	slackSummary(summary)
  }
  
  function getSummaryFromChatGpt() {
	var journal = extractTextFromGoogleDoc()
	var prompt = "Please summarize the following journal: " + journal;
	var answer = askChatGpt(prompt)
	return answer;
  }
  
  function extractTextFromGoogleDoc() {
	var doc = DocumentApp.getActiveDocument();
	var body = doc.getBody();
	var text = body.getText();
	return text
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
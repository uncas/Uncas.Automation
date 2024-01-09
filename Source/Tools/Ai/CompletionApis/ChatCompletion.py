def getChatCompletion(messages):
	chatCompletionUrl = "http://127.0.0.1:5000/v1/chat/completions"
	headers = { "Content-Type": "application/json" }
	data = {
        "mode": "chat",
        "character": "Assistant",
        "messages": messages
    }
	import requests
	response = requests.post(chatCompletionUrl, headers = headers, json = data, verify = False)
	responseContent = response.json()
	#import json
	#print(json.dumps(responseContent, indent = 2))
	return responseContent
	
def getAndAppendChatCompletion(message, messages):
    messages.append({"role": "user", "content": message})
    responseContent = getChatCompletion(messages)
    assistantMessage = responseContent['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": assistantMessage})
    return responseContent

def startChat():
	messages = [{"role": "system", "content": "You are a helpful assistant."}]
	return messages

def getSingleChatCompletion(message):
	messages = startChat()
	getAndAppendChatCompletion(message, messages)
	return messages[-1]['content']

def askQuestion():
	print("Ask a question:")
	message = input("> ")
	print(getSingleChatCompletion(message))

def chat():
	quitInfo = "(Press q to quit)"
	print("Welcome to the chat! " + quitInfo)
	messages = startChat()
	while True:
		message = input("> ")
		if message == "q": return
		if not message: continue
		responseContent = getAndAppendChatCompletion(message, messages)
		print(messages[-1]['content'])
		print(quitInfo)

if __name__ == "__main__":
	askQuestion()

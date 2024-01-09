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

def getSingleChatCompletion(message):
	messages = [{"role": "system", "content": "You are a helpful assistant."}]
	getAndAppendChatCompletion(message, messages)
	return messages[-1]['content']

if __name__ == "__main__":
	print("Welcome to the chat!")
	message = input("> ")
	print(getSingleChatCompletion(message))

def askChatGpt(messages):
	from openai import OpenAI
	from Utils.Settings import getSetting
	apiKey = getSetting("openAi")["apiKey"]
	client = OpenAI(api_key=apiKey)
	chat = client.chat.completions.create( 
		model="gpt-3.5-turbo", messages = messages 
	)
	reply = chat.choices[0].message.content 
	return reply

def runChatGpt():
	messages = [ {"role": "system", "content": "You are an intelligent assistant."} ]
	while True: 
		message = input("User : ")
		if message:
			messages.append( 
				{"role": "user", "content": message}, 
			)
			reply = askChatGpt(messages)
			print(f"ChatGPT: {reply}") 
			messages.append({"role": "assistant", "content": reply})

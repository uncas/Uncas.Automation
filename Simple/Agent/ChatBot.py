class ChatBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})
    
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        return self.executeOpenAi()

    def executeOllama(self):
        import ollama
        response = ollama.chat(model='llama3', messages=self.messages)
        return response['message']['content']

    def executeOpenAi(self):
        from openai import OpenAI
        client = OpenAI()
        completion = client.chat.completions.create(messages=self.messages, model="gpt-3.5-turbo")
        print(completion.usage)
        return completion.choices[0].message.content

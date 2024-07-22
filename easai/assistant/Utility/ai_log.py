class AiLog:
	def __init__(self):
		import sqlite3
		self.db = sqlite3.connect("Data/AiLog.db")
		self.db.execute("CREATE TABLE IF NOT EXISTS AiLog (AiLogId INTEGER PRIMARY KEY, Date TEXT, Model TEXT, PromptTokens INTEGER, CompletionTokens INTEGER, Messages TEXT, TimeStamp INTEGER)")

	def log(self, model, promptTokens, completionTokens, messages):
		import json
		from datetime import datetime
		now = datetime.now()
		timeStamp = int(now.timestamp())
		isoString = now.isoformat()
		messagesString = json.dumps([self.extract_message_values(message) for message in messages])
		self.db.execute(
			"INSERT INTO AiLog (AiLogId, Date, Model, PromptTokens, CompletionTokens, Messages, TimeStamp) VALUES (?, ?, ?, ?, ?, ?, ?)", 
			(None, isoString, model, promptTokens, completionTokens, messagesString, timeStamp))
		self.db.commit()

	def extract_message_values(self, message):
		from openai.types.chat.chat_completion_message import ChatCompletionMessage
		if isinstance(message, ChatCompletionMessage):
			return {
				"role": message.role, 
				"content": message.content,
				"tool_calls": [self.extract_tool_call_values(toolCall) for toolCall in message.tool_calls] if message.tool_calls else None
			}
		return {
			"role": message["role"],
			"content": message["content"],
			"name": message["name"] if "name" in message else None,
			"tool_call_id": message["tool_call_id"] if "tool_call_id" in message else None
		}
	
	def extract_tool_call_values(self, toolCall):
		return {
			"id": toolCall.id,
			"functionName": toolCall.function.name, 
		  	"arguments": toolCall.function.arguments
		}

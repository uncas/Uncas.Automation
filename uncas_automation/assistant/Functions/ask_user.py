def ask_user(question):
	return input(question)

def ask_user_tool():
	from easai.assistant.tool import AssistantTool, AssistantToolParameter
	return AssistantTool(ask_user, "Ask user", [
		AssistantToolParameter("question", "What you want to ask me about")
	])

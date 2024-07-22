def ask_user(data):
	question = data["question"]
	return input(question)

def ask_user_tool():
	from easai.Flows.PersonalAssistant.assistant_tools import AssistantTool, AssistantToolParameter
	return AssistantTool(ask_user, "Ask user", [
		AssistantToolParameter("question", "What you want to ask me about")
	])

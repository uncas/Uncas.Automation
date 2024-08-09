def save_to_file(data):
	from uncas_automation.Utils.FileUtils import write_text
	import datetime
	text = data["text"]
	file_name = data["file_name"]
	file_name = "assistant_save_" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + "_" + file_name
	write_text("Output", file_name, text)

def save_to_file_tool():
	from uncas_automation.assistant.assistant_tools import AssistantTool, AssistantToolParameter
	return AssistantTool(save_to_file, "Save text content to a file", [
		AssistantToolParameter("text", "The text content to save"),
		AssistantToolParameter("file_name", "The name of the file to save to, for example 'plan.html'.")
	])
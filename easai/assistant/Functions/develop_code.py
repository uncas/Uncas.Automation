import os

from easai.Utils.FileUtils import write_text

def save_code(data):
	code = data["code"]
	folder_path = data["folder_path"]
	file_name = data["file_name"]
	full_folder_path = os.path.join("Output/assistant_code", folder_path)
	write_text(full_folder_path, file_name, code)

def save_code_tool():
	from easai.assistant.assistant_tools import AssistantTool, AssistantToolParameter
	return AssistantTool(save_code, "Save code", [
		AssistantToolParameter("code", "The code"),
		AssistantToolParameter("folder_path", "The path to the folder where the code should be saved."),
		AssistantToolParameter("file_name", "The name of the file to contain the code.")
	])

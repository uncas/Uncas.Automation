import os

from easai.utils.file_utils import write_text

code_base_path = "Output/assistant_code"

def save_code(data):
	code = data["code"]
	folder_path = data["folder_path"]
	file_name = data["file_name"]
	full_folder_path = os.path.join(code_base_path, folder_path)
	write_text(full_folder_path, file_name, code)

def read_code():
	code = ""
	files = os.listdir(code_base_path)
	for file in files:
		code += "FILE: " + file + ":\n"
		file_path = os.path.join(code_base_path, file)
		with open(file_path, "r") as file:
			code += file.read()
			code += "\n\n\n\n"
	return code

def save_code_tool():
	from uncas_automation.assistant.assistant_tools import AssistantTool, AssistantToolParameter
	return AssistantTool(save_code, "Save code", [
		AssistantToolParameter("code", "The code"),
		AssistantToolParameter("folder_path", "The path to the folder where the code should be saved."),
		AssistantToolParameter("file_name", "The name of the file to contain the code.")
	])

def read_code_tool():
	from uncas_automation.assistant.assistant_tools import AssistantTool
	return AssistantTool(read_code, "Read code")
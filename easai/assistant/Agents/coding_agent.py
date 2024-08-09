from easai.assistant.Agents.agent_definition import AgentDefinition

class CodingAgent(AgentDefinition):
	def __init__(self):
		system_prompt_file = "Coder-system.md"
		system_prompt = AgentDefinition.get_system_prompt_from_file(system_prompt_file)
		input_tasks = []
		scenario = input("What should I code?")
		input_tasks.append({ "task": lambda: scenario, "prompt": "What to code" })
		action_on_result = self.print_done
		super().__init__(system_prompt, input_tasks, action_on_result, tools = self.get_tools())

	def print_done(self, output):
		print("DONE")

	def get_tools(self):
		from easai.assistant.Functions.develop_code import save_code_tool, read_code_tool

		return [
			save_code_tool(),
			read_code_tool()
		]

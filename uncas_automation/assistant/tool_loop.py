import json
import logging

from openai import OpenAI

from uncas_automation.assistant.Utility.ai_log import AiLogBase, LoggingAiLog

def run_tool_loop(
		client: OpenAI,
		tools: list,
		messages: list,
		model: str,
		max_iterations: int = 10,
		assistant_message_callback = None,
		tool_message_callback = None,
		ai_logger: AiLogBase = LoggingAiLog()) -> list:
	client_tools = [tool.map_to_open_ai_tool() for tool in tools]
	tool_methods = {tool.name: tool.method for tool in tools}
	message_count_at_last_log = len(messages) - 1
	for _ in range(max_iterations):
		chat_completion = client.chat.completions.create(
			messages = messages,
			model = model,
			tools = client_tools
		)
		choice = chat_completion.choices[0]
		finish_reason = choice.finish_reason
		message = choice.message
		messages.append(message)
		ai_logger.log(model, chat_completion.usage.prompt_tokens, chat_completion.usage.completion_tokens, messages[message_count_at_last_log:])
		message_count_at_last_log = len(messages)
		if finish_reason == "stop":
			if assistant_message_callback:
				assistant_message_callback(message.content)
			return messages
		elif finish_reason == "tool_calls":
			for tool_call in message.tool_calls:
				call_function = tool_call.function
				if call_function.name in tool_methods:
					function_name = call_function.name
					function_args = json.loads(call_function.arguments)
					function_response = None
					tool_method = tool_methods[function_name]
					if function_args:
						if tool_message_callback:
							tool_message_callback("Calling function " + function_name + " with " + str(function_args))
						function_response = tool_method(function_args)
					else:
						if tool_message_callback:
							tool_message_callback("Calling function " + function_name)
						function_response = tool_method()
					messages.append({
						"role": "tool",
						"name": function_name,
						"tool_call_id": tool_call.id,
						"content": get_limited_message_content(json.dumps(function_response))
					})
	logger = logging.getLogger(__name__)
	logger.error("ERROR: Tool loop exited without stop reason, most likely due to too many iterations.")
	return messages

def get_limited_message_content(content, max_message_content_length = 100 * 1000):
	if len(content) <= max_message_content_length:
		return content

	logger = logging.getLogger(__name__)
	logger.warning(
		"Message content %s was too long, truncating to %d characters.",
		content[:50] + " ... " + content[-50:],
		max_message_content_length)
	return content[:max_message_content_length] + "..."

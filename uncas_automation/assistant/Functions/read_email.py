def read_email():
	from uncas_automation.Services.Google.GmailService import getInboxMessages
	messages = getInboxMessages()
	result = [{
		"sender": message["sender"], 
		"date": message["date"], 
		"subject": message["subject"], 
		"body": message["body"],
		"internalMessageId": message["internalMessageId"]
	} for message in messages]
	return result

def writeEmail(data):
	from uncas_automation.Services.Google.GmailSendService import createDraft
	body = data["body"]
	subject = data["subject"]
	recipient = data["recipient"]
	internalMessageId = data["internalMessageId"] if "internalMessageId" in data else None
	createDraft(recipient, subject, body, internalMessageId)

def write_email_tool():
	from uncas_automation.assistant.assistant_tools import AssistantTool, AssistantToolParameter
	return AssistantTool(writeEmail, "Write an email", [
		AssistantToolParameter("recipient", "The recipient of the email"),
		AssistantToolParameter("subject", "The subject of the email"),
		AssistantToolParameter("body", "The body of the email"),
		AssistantToolParameter("internalMessageId", "The internal id of the message that should be replied to (used only when replying to an email)")
	])

def read_email_tool():
	from uncas_automation.assistant.assistant_tools import AssistantTool
	return AssistantTool(read_email, "Read email")
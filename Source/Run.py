def isInVirtualEnvironment():
	import sys
	return sys.prefix != sys.base_prefix

def run():
	if not isInVirtualEnvironment():
		print("Virtual environment not enabled. Exiting...")
		return

	while True:
		print("Menu:")

		tasks = [
			{"id": "1", "name": "Ask question"},
			{"id": "2", "name": "Chat"},
			{"id": "3", "name": "Question docs from sheet list"},
			{"id": "4", "name": "Assist with emails"},
			{"id": "5", "name": "Ask ChatGpt"},
			{"id": "T", "name": "Test all"},
			{"id": "Q", "name": "Quit"}
			]

		menu = "\n".join(map(lambda task: task["id"] + ") " + task["name"], tasks))
		task = input(menu + "\nEnter your choice: ").lower()

		if task == "1":
			from Tools.Ai.CompletionApis.ChatCompletion import askQuestion
			askQuestion()
		elif task == "2":
			from Tools.Ai.CompletionApis.ChatCompletion import chat
			chat()
		elif task == "3":
			from Flows.QuestionGoogleDocsFromSheetList import runQuestionGoogleDocsFromSheetList
			runQuestionGoogleDocsFromSheetList()
		elif task == "4":
			from Flows.MailAssistant import assistWithMails
			assistWithMails()
		elif task == "5":
			from Services.OpenAi.ChatGptService import runChatGpt
			runChatGpt()
		elif task == "t":
			from Services.Google.GmailServiceTests import testGmailService
			testGmailService()

			return
			from QuestionGoogleDocsFromSheetListTests import testQuestionGoogleDocsFromSheetList
			testQuestionGoogleDocsFromSheetList()
	
			from Services.Google.GooglePresentationsServiceTests import testGooglePresentationsService
			testGooglePresentationsService()

			from QuestionGoogleDocTests import testQuestionGoogleDoc
			from Services.Google.GoogleDocsServiceTests import testGoogleDocsService
			from Services.Google.GoogleSheetsServiceTests import testGoogleSheetsService
			from Tools.Ai.QaPipelineTests import testQaPipeline
			from Tools.Ai.QueryLMTests import testQueryLM
			testGoogleDocsService()
			testGoogleSheetsService()
			testQueryLM()
			testQaPipeline()
			testQuestionGoogleDoc()
		elif task == "q":
			return
		else:
			print("Not implemented")
		print()

if __name__ == "__main__":
	run()
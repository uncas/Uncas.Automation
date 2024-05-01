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
			{"id": "6", "name": "Create image with huggingface"},
			{"id": "7", "name": "Generate text with huggingface"},
			{"id": "8", "name": "Classify text with huggingface"},
			{"id": "9", "name": "Translate with huggingface"},
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
		elif task == "6":
			from Services.HuggingFace.HuggingFaceService import runCreateImage
			runCreateImage()
		elif task == "7":
			from Services.HuggingFace.HuggingFaceService import generateText
			generateText()
		elif task == "8":
			from Services.HuggingFace.HuggingFaceService import classifyText
			classifyText()
		elif task == "9":
			from Services.HuggingFace.HuggingFaceService import translate
			translate()
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
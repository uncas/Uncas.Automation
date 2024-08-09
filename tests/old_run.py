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
			{"id": "5", "name": "Ask ChatGpt"},
			{"id": "6", "name": "Create image with huggingface"},
			{"id": "7", "name": "Generate text with huggingface"},
			{"id": "8", "name": "Classify text with huggingface"},
			{"id": "9", "name": "Translate with huggingface"},
			{"id": "10", "name": "Speak text with huggingface"},
			{"id": "11", "name": "Search with huggingface"},
			{"id": "12", "name": "Read cars from Bilbasen blog"},
			{"id": "13", "name": "Embeddings with openai"},
			{"id": "14", "name": "Split text with langchain"},
			{"id": "15", "name": "Embed locally"},
			{"id": "T", "name": "Test all"},
			{"id": "Q", "name": "Quit"}
			]

		menu = "\n".join(map(lambda task: task["id"] + ") " + task["name"], tasks))
		task = input(menu + "\nEnter your choice: ").lower()

		if task == "1":
			from uncas_automation.Tools.Ai.CompletionApis.ChatCompletion import askQuestion
			askQuestion()
		elif task == "2":
			from uncas_automation.Tools.Ai.CompletionApis.ChatCompletion import chat
			chat()
		elif task == "3":
			from uncas_automation.Flows.QuestionGoogleDocsFromSheetList import runQuestionGoogleDocsFromSheetList
			runQuestionGoogleDocsFromSheetList()
		elif task == "5":
			from uncas_automation.Services.OpenAi.ChatGptService import runChatGpt
			runChatGpt()
		elif task == "6":
			from uncas_automation.Services.HuggingFace.HuggingFaceService import runCreateImage
			runCreateImage()
		elif task == "7":
			from uncas_automation.Services.HuggingFace.HuggingFaceService import generateText
			generateText()
		elif task == "8":
			from uncas_automation.Services.HuggingFace.HuggingFaceService import classifyText
			classifyText()
		elif task == "9":
			from uncas_automation.Services.HuggingFace.HuggingFaceService import translate
			translate()
		elif task == "10":
			from uncas_automation.Services.HuggingFace.HuggingFaceService import runSpeak
			runSpeak()
		elif task == "11":
			from uncas_automation.Services.HuggingFace.HuggingFaceService import search
			search()
		elif task == "12":
			from uncas_automation.Services.eletric_cars_service import get_electric_cars_in_denmark
			get_electric_cars_in_denmark()
		elif task == "13":
			from uncas_automation.Services.OpenAi.EmbeddingService import runGetEmbedding
			runGetEmbedding()
		elif task == "14":
			from uncas_automation.Services.LangChain.TextSplitter import runSplitText
			runSplitText()
		elif task == "15":
			from uncas_automation.Services.Embeddings.Embeddor import runEmbed
			runEmbed()
		elif task == "t":
			from tests.test_GmailService_adhoc import testGmailService
			testGmailService()

			return
			from QuestionGoogleDocsFromSheetListTests import testQuestionGoogleDocsFromSheetList
			testQuestionGoogleDocsFromSheetList()
	
			from uncas_automation.Services.Google.GooglePresentationsServiceTests import testGooglePresentationsService
			testGooglePresentationsService()

			from QuestionGoogleDocTests import testQuestionGoogleDoc
			from uncas_automation.Services.Google.GoogleDocsServiceTests import test_readDocument
			from uncas_automation.Services.Google.GoogleSheetsServiceTests import testGoogleSheetsService
			from uncas_automation.Tools.Ai.QaPipelineTests import testQaPipeline
			from uncas_automation.Tools.Ai.QueryLMTests import testQueryLM
			test_readDocument()
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
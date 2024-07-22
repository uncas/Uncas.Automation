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
			from easai.Tools.Ai.CompletionApis.ChatCompletion import askQuestion
			askQuestion()
		elif task == "2":
			from easai.Tools.Ai.CompletionApis.ChatCompletion import chat
			chat()
		elif task == "3":
			from easai.Flows.QuestionGoogleDocsFromSheetList import runQuestionGoogleDocsFromSheetList
			runQuestionGoogleDocsFromSheetList()
		elif task == "5":
			from easai.Services.OpenAi.ChatGptService import runChatGpt
			runChatGpt()
		elif task == "6":
			from easai.Services.HuggingFace.HuggingFaceService import runCreateImage
			runCreateImage()
		elif task == "7":
			from easai.Services.HuggingFace.HuggingFaceService import generateText
			generateText()
		elif task == "8":
			from easai.Services.HuggingFace.HuggingFaceService import classifyText
			classifyText()
		elif task == "9":
			from easai.Services.HuggingFace.HuggingFaceService import translate
			translate()
		elif task == "10":
			from easai.Services.HuggingFace.HuggingFaceService import runSpeak
			runSpeak()
		elif task == "11":
			from easai.Services.HuggingFace.HuggingFaceService import search
			search()
		elif task == "12":
			from easai.Services.eletric_cars_service import get_electric_cars_in_denmark
			get_electric_cars_in_denmark()
		elif task == "13":
			from easai.Services.OpenAi.EmbeddingService import runGetEmbedding
			runGetEmbedding()
		elif task == "14":
			from easai.Services.LangChain.TextSplitter import runSplitText
			runSplitText()
		elif task == "15":
			from easai.Services.Embeddings.Embeddor import runEmbed
			runEmbed()
		elif task == "t":
			from tests.test_GmailService_adhoc import testGmailService
			testGmailService()

			return
			from QuestionGoogleDocsFromSheetListTests import testQuestionGoogleDocsFromSheetList
			testQuestionGoogleDocsFromSheetList()
	
			from easai.Services.Google.GooglePresentationsServiceTests import testGooglePresentationsService
			testGooglePresentationsService()

			from QuestionGoogleDocTests import testQuestionGoogleDoc
			from easai.Services.Google.GoogleDocsServiceTests import test_readDocument
			from easai.Services.Google.GoogleSheetsServiceTests import testGoogleSheetsService
			from easai.Tools.Ai.QaPipelineTests import testQaPipeline
			from easai.Tools.Ai.QueryLMTests import testQueryLM
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
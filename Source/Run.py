from QuestionGoogleDocTests import testQuestionGoogleDoc
from Services.Google.GoogleDocsServiceTests import testGoogleDocsService
from Services.Google.GooglePresentationsServiceTests import testGooglePresentationsService
from Services.Google.GoogleSheetsServiceTests import testGoogleSheetsService
from Tools.Ai.QaPipelineTests import testQaPipeline
from Tools.Ai.QueryLMTests import testQueryLM

def run():
	while True:
		print("Menu:")

		tasks = [
			{"id": "1", "name": "Ask question"},
			{"id": "2", "name": "Chat"},
			{"id": "T", "name": "Test all"},
			{"id": "Q", "name": "Quit"}
			]

		menu = "\n".join(map(lambda task: task["id"] + ") " + task["name"], tasks))
		task = input(menu + "\nEnter your choice: ").lower()

		if task == "t":
			testGooglePresentationsService()
			return
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
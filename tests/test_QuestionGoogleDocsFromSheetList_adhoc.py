from easai.Flows.QuestionGoogleDocsFromSheetList import questionGoogleDocsFromSheetList

def testQuestionGoogleDocsFromSheetList():
	sheetId = "xx"
	question = input("Question: ")
	answer = questionGoogleDocsFromSheetList(sheetId, "Ark1!D2:D", question)
	print("Answer: " + answer)

if __name__ == "__main__":
	testQuestionGoogleDocsFromSheetList()
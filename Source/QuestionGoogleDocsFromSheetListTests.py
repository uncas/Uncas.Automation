from Flows.QuestionGoogleDocsFromSheetList import questionGoogleDocsFromSheetList

def testQuestionGoogleDocsFromSheetList():
	sheetId = "1X9QhUocllUsrhW07g2X2O3CqBuURAFMXBqmjqkePvN8"
	question = "Which tools do we use for documentation?"
	answer = questionGoogleDocsFromSheetList(sheetId, "Ark1!D2:D", question)
	print("Answer: " + answer)

if __name__ == "__main__":
	testQuestionGoogleDocsFromSheetList()
from Flows.QuestionGoogleDocsFromSheetList import questionGoogleDocsFromSheetList

def testQuestionGoogleDocsFromSheetList():
	sheetId = "1X9QhUocllUsrhW07g2X2O3CqBuURAFMXBqmjqkePvN8"
	question = "Which tools do we use for documentation?"
	answers = questionGoogleDocsFromSheetList(sheetId, "Ark1!D2:D", question)
	print(answers)

if __name__ == "__main__":
	testQuestionGoogleDocsFromSheetList()
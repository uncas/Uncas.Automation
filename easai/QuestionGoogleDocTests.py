from easai.Flows.QuestionGoogleDoc import questionGoogleDoc

def testQuestionGoogleDoc():
	id = "xx"
	question = "Which tools do we use for documentation?"
	answers = questionGoogleDoc(id, question)
	print(answers)

if __name__ == "__main__":
	testQuestionGoogleDoc()
from Flows.QuestionGoogleDoc import questionGoogleDoc

def testQuestionGoogleDoc():
	id = "1j80Lx1Rlu3w1gOh6FHZeF3TftA4vyV9VNEyskpF6wO4"
	question = "Which tools do we use for documentation?"
	answers = questionGoogleDoc(id, question)
	print(answers)

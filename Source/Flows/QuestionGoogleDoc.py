from Services.Google.GoogleDocsService import readDocument
from Utils.FileUtils import writeText
import Tools.Ai.QaPipeline

def questionGoogleDoc(id, question):
	doc = readDocument(id)
	folder = "Data/GoogleDoc/" + id
	writeText(folder, "doc.txt", doc["text"])
	return Tools.Ai.QaPipeline.questionDocuments(folder, question)

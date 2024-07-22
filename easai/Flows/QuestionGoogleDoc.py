from Services.Google.GoogleDocsService import readDocument
from Utils.FileUtils import write_text
import Tools.Ai.QaPipeline

def questionGoogleDoc(id, question):
	doc = readDocument(id)
	folder = "Data/GoogleDoc/" + id
	write_text(folder, "doc.txt", doc["text"])
	return Tools.Ai.QaPipeline.questionDocuments(folder, question)

from Services.Google.GoogleDocsService import readDocument
import Tools.Ai.QaPipeline

def questionGoogleDoc(id, question):
	doc = readDocument(id)
	folder = "Data/GoogleDoc/" + id
	from pathlib import Path
	Path(folder).mkdir(parents=True, exist_ok=True)
	f = open(folder + "/doc.txt", "w")
	f.write(doc["text"])
	f.close()
	return Tools.Ai.QaPipeline.questionDocuments(folder, question)

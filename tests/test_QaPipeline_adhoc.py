import ssl
from uncas_automation.Tools.Ai.QaPipeline import questionDocuments
from haystack.utils import fetch_archive_from_http

def testQaPipeline():
	documentDirectory = "Data/GameOfThrones"

	try:
		_create_unverified_https_context = ssl._create_unverified_context
	except AttributeError:
		pass
	else:
		ssl._create_default_https_context = _create_unverified_https_context


	url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt1.zip"
	fetch_archive_from_http(url = url, output_dir = documentDirectory)
	question = "What's the name of Cersei's children?"
	question = "Who is Arya's father?"
	answers = questionDocuments(documentDirectory, question)
	print(answers)
from QaPipeline import questionDocuments
from haystack.utils import fetch_archive_from_http

documentDirectory = "Data/GameOfThrones"
url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt1.zip"
fetch_archive_from_http(url = url, output_dir = documentDirectory)
question = "What's the name of Cersei's children?"
questionDocuments(documentDirectory, question)

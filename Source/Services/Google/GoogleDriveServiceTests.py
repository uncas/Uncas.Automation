def test_exportDocumentAsMarkdown():
	from Services.Google.GoogleDriveService import exportDocumentAsMarkdown
	id = "blabla"
	result = exportDocumentAsMarkdown(id)
	from Utils.FileUtils import writeText
	print(result[:2000])
	writeText("Output", "doc.md", result)

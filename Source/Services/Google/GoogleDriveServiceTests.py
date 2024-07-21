def test_exportDocumentAsMarkdown():
	from Services.Google.GoogleDriveService import exportDocumentAsMarkdown
	id = "blabla"
	result = exportDocumentAsMarkdown(id)
	from Utils.FileUtils import write_text
	print(result[:2000])
	write_text("Output", "doc.md", result)

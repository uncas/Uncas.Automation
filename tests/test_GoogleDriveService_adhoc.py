def test_exportDocumentAsMarkdown():
	from uncas_automation.Services.Google.GoogleDriveService import exportDocumentAsMarkdown
	id = "blabla"
	result = exportDocumentAsMarkdown(id)
	from easai.utils.file_utils import write_text
	print(result[:2000])
	write_text("Output", "doc.md", result)

# https://developers.google.com/drive/api/guides/manage-downloads

def exportDocumentAsHtml(documentId):
	from googleapiclient.discovery import build
	from googleapiclient.errors import HttpError
	from Services.Google.GoogleAuth import getCredentials
	creds = getCredentials()
	try:
		service = build("drive", "v3", credentials=creds)
		request = service.files().export_media(fileId=documentId, mimeType="text/html")
		response = request.execute()
		return response
	except HttpError as err:
		print(err)

def exportDocumentAsMarkdown(documentId):
	import html2text
	html = exportDocumentAsHtml(documentId).decode("utf-8")
	return html2text.html2text(html)

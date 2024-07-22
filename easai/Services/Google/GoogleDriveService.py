# https://developers.google.com/drive/api/guides/manage-downloads

def exportDocumentAsHtml(documentId):
	from googleapiclient.discovery import build
	from googleapiclient.errors import HttpError
	from easai.Services.Google.GoogleAuth import getCredentials
	creds = getCredentials()
	try:
		service = build("drive", "v3", credentials=creds)
		request = service.files().export_media(fileId=documentId, mimeType="text/html")
		response = request.execute()
		return response
	except HttpError as err:
		print(err)

def exportDocumentAsMarkdown(documentId):
	# https://github.com/Alir3z4/html2text/blob/master/docs/usage.md
	import html2text
	textMaker = html2text.HTML2Text()
	html = exportDocumentAsHtml(documentId).decode("utf-8")
	return textMaker.handle(html)

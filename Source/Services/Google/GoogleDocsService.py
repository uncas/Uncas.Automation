# From: https://developers.google.com/docs/api/quickstart/python
# From: https://developers.google.com/docs/api/samples/extract-text

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from Services.Google.GoogleAuth import getCredentials

def getDocumentTexts(documentId):
  creds = getCredentials()
  try:
    service = build("docs", "v1", credentials=creds)
    document = service.documents().get(documentId=documentId).execute()
    title = document.get('title')
    content = document.get('body').get('content')
    #from Utils.FileUtils import writeText
    #import json
    #writeText("Test", "GoogleDocContent.json", json.dumps(content, indent = 4))
    return {"title": title, "texts": getListOfTextContent(content)}
  except HttpError as err:
    print(err)

def readDocument(documentId):
    texts = getDocumentTexts(documentId)
    text = "".join([item["text"] for item in texts["texts"]])
    return {"title": texts["title"], "text": text};

def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')

def read_structural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    return "".join([item["text"] for item in getListOfTextContent(elements)])

def getListOfTextContent(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    result = []
    for value in elements:
        if 'paragraph' in value:
            paragraph = value.get('paragraph')
            elements = paragraph.get('elements')
            paragraphStyle = paragraph.get('paragraphStyle').get('namedStyleType')
            for elem in elements:
                result.append({"text": read_paragraph_element(elem), "type": "paragraph", "style": paragraphStyle})
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    result.append({"text": read_structural_elements(cell.get('content')), "type": "cell"})
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            result.append({"text": read_structural_elements(toc.get('content')), "type": "toc"})
    return result
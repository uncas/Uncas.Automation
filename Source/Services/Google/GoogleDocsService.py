# From: https://developers.google.com/docs/api/quickstart/python
# From: https://developers.google.com/docs/api/samples/extract-text

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from Services.Google.GoogleAuth import getCredentials

def readDocument(documentId):
  creds = getCredentials()
  try:
    service = build("docs", "v1", credentials=creds)
    document = service.documents().get(documentId=documentId).execute()
    title = document.get('title')
    content = document.get('body').get('content')
    text = read_structural_elements(content)
    return {"title": title, "text": text};
  except HttpError as err:
    print(err)

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
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_structural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_structural_elements(toc.get('content'))
    return text
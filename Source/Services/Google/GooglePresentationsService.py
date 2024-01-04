# From: https://developers.google.com/docs/api/quickstart/python
# From: https://developers.google.com/docs/api/samples/extract-text

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from Services.Google.GoogleAuth import getCredentials

def readPresentation(presentationId):
  creds = getCredentials()
  try:
    service = build("slides", "v1", credentials=creds)
    presentation = (service.presentations().get(presentationId=presentationId).execute())
    textContent = getTextContent(presentation)
    return { "title": presentation["title"], "text": textContent }

  except HttpError as err:
    print(err)

def getTextContent(presentation):
  slides = presentation.get("slides")
  result = []
  for slide in slides:
    elements = slide.get('pageElements')
    result = result + flatten(getContentOfElements(elements))
  return "\n".join(result)

def getContentOfElements(elements):
    if (elements == None):
      return
    for element in elements:
        if "shape" in element:
          yield getTexts(element["shape"])
        if "table" in element:
          rows = element["table"]["tableRows"]
          cells = flatten(map(getCells, rows))
          texts = map(lambda cell: getTexts(cell), cells)
          yield flatten(texts)
        if "elementGroup" in element:
          yield flatten(getContentOfElements(element["elementGroup"]["children"]))

def getCells(row):
  if "tableCells" in row:
    return row["tableCells"]
  return []

def getTexts(shapeOrCell):
  if "text" not in shapeOrCell:
    return

  textElements = shapeOrCell["text"]["textElements"]
  for e in textElements:
    if "textRun" in e:
      yield e["textRun"]["content"]

def flatten(xss):
  return [x for xs in xss for x in xs]

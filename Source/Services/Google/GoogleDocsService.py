# From # https://developers.google.com/docs/api/quickstart/python
#https://developers.google.com/docs/api/samples/extract-text

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file GoogleToken.json.
SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]

def readDocument(documentId):
  credentialsFile = "Config/GoogleCredentials.json"
  if not os.path.exists(credentialsFile):
     raise Exception("No Google credentials file exists. \
Follow guideline here https://developers.google.com/docs/api/quickstart/python \
to create credentials, and then download and place credentials file here: " + credentialsFile)
  
  creds = None
  # The file GoogleToken.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  tokenFile = "Config/GoogleToken.json"
  if os.path.exists(tokenFile):
    creds = Credentials.from_authorized_user_file(tokenFile, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(credentialsFile, SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(tokenFile, "w") as token:
      token.write(creds.to_json())

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
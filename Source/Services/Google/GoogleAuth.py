# From # https://developers.google.com/docs/api/quickstart/python

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def getCredentials():
  scopes = ["documents.readonly", "spreadsheets.readonly", "presentations.readonly", "gmail.readonly", "gmail.compose", "calendar.readonly"]
  tokenFile = "Config/GoogleToken_" + "-".join(scopes) + ".json"
  credentialsFile = "Config/GoogleCredentials.json"
  if not os.path.exists(credentialsFile):
     raise Exception("No Google credentials file exists. \
Follow guideline here https://developers.google.com/docs/api/quickstart/python \
to create credentials, and then download and place credentials file here: " + credentialsFile)
  
  fullScopes = list(map(lambda s: "https://www.googleapis.com/auth/" + s, scopes))
  creds = None
  # The file GoogleToken.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first time.
  if os.path.exists(tokenFile):
    creds = Credentials.from_authorized_user_file(tokenFile, fullScopes)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(credentialsFile, fullScopes)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(tokenFile, "w") as token:
      token.write(creds.to_json())

  return creds

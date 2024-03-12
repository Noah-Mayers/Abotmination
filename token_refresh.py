import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID of a sample document.
DOCUMENT_ID = "1s2rE7cu9HWaFUAnVoRmri7hmo-Kj2w0ri9yq6W0ebDE"
DOCUMENT_RANGE = "Heroes!A1:U"


def main():
  """Shows basic usage of the Docs API.
  Prints the title of a sample document.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build( "sheets", "v4", 
      credentials=Credentials.from_authorized_user_file("token.json", SCOPES),
      client_options={"quota_project_id": "abotmination"}
      )
    
    # Retrieve the documents contents from the Docs service.
    document = (service.spreadsheets().values().get(spreadsheetId=DOCUMENT_ID, range=DOCUMENT_RANGE).execute()).get('values', [])

    print(f"The data requested is: {document}")
  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()
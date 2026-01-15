import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from config import SHEETS_SCOPES

def get_sheets_service():
    creds = None
    token_path = "credentials/token_sheets.pickle"

    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials/credentials.json", SHEETS_SCOPES
        )
        creds = flow.run_local_server(port=0)
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return build("sheets", "v4", credentials=creds)

def append_row(service, spreadsheet_id, sheet_name, row):
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=sheet_name,
        valueInputOption="RAW",
        body={"values": [row]}
    ).execute()

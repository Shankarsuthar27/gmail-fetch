from gmail_service import get_gmail_service, fetch_unread_emails
from sheets_service import get_sheets_service, append_row
from email_parser import parse_email
from config import SPREADSHEET_ID, SHEET_NAME, STATE_FILE
import os

def load_processed_ids():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE, "r") as f:
        return set(f.read().splitlines())

def save_processed_id(msg_id):
    with open(STATE_FILE, "a") as f:
        f.write(msg_id + "\n")

def mark_as_read(service, msg_id):
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()

def main():
    gmail = get_gmail_service()
    sheets = get_sheets_service()

    processed = load_processed_ids()
    messages = fetch_unread_emails(gmail)

    for msg in messages:
        if msg["id"] in processed:
            continue

        data = parse_email(gmail, msg["id"])
        row = [
            data["from"],
            data["subject"],
            data["date"],
            data["content"]
        ]

        append_row(sheets, SPREADSHEET_ID, SHEET_NAME, row)
        save_processed_id(msg["id"])
        mark_as_read(gmail, msg["id"])

if __name__ == "__main__":
    main()

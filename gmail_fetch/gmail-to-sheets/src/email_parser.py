import base64

def parse_email(service, msg_id):
    msg = service.users().messages().get(
        userId="me", id=msg_id, format="full"
    ).execute()

    headers = msg["payload"]["headers"]
    data = {}

    for h in headers:
        if h["name"] == "From":
            data["from"] = h["value"]
        if h["name"] == "Subject":
            data["subject"] = h["value"]
        if h["name"] == "Date":
            data["date"] = h["value"]

    parts = msg["payload"].get("parts", [])
    body = ""

    for part in parts:
        if part["mimeType"] == "text/plain":
            body = base64.urlsafe_b64decode(
                part["body"]["data"]
            ).decode("utf-8")

    data["content"] = body.strip()
    return data

import base64

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from services.gmail_auth import ensure_credentials


def create_gmail_service():
    return build("gmail", "v1", credentials=ensure_credentials())


def fetch_email_metadata(service, max_results=10):
    """Fetch list of email message IDs"""
    try:
        result = (
            service.users()
            .messages()
            .list(userId="me", maxResults=max_results)
            .execute()
        )
        return result.get("messages", [])
    except HttpError as error:
        raise Exception(f"Gmail API error: {error}") from error


def get_email_details(service, message_id):
    """Get full email details by message ID"""
    try:
        return (
            service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )
    except HttpError as error:
        raise Exception(f"Gmail API error: {error}") from error


def parse_email_headers(headers, target):
    """Extract specific header from email headers"""
    return next((h["value"] for h in headers if h["name"] == target), "N/A")


def decode_email_body(part):
    """Decode base64 encoded email body"""
    return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")


def process_email_parts(parts):
    """Extract plain and HTML bodies from email parts"""
    bodies = {"plain": "", "html": ""}
    for part in parts:
        if part["mimeType"] == "text/plain":
            bodies["plain"] = decode_email_body(part)
        elif part["mimeType"] == "text/html":
            bodies["html"] = decode_email_body(part)
    return bodies

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from services.gmail.auth import ensure_credentials


def create_gmail_service():
    return build("gmail", "v1", credentials=ensure_credentials())


def fetch_email_metadata(service, max_results=10):
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


def fetch_email_details(service, email_id):
    try:
        return (
            service.users()
            .messages()
            .get(userId="me", id=email_id, format="full")
            .execute()
        )
    except HttpError as error:
        raise Exception(f"Gmail API error: {error}") from error

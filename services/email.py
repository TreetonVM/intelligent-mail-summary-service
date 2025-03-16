from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.parsing import EmailData, parse_email

from .auth import get_credentials


def create_gmail_service():
    """Factory function for service creation"""
    return build("gmail", "v1", credentials=get_credentials())


def fetch_emails(
    service, max_results: int = 10
) -> tuple[list[EmailData], Exception | None]:
    """Main workflow composed from pure functions"""
    try:
        messages = get_message_ids(service, max_results)
        return [process_message(service, msg["id"]) for msg in messages], None
    except HttpError as e:
        return [], e


def get_message_ids(service, max_results: int) -> list[dict]:
    """Pure function for message listing"""
    return (
        service.users()
        .messages()
        .list(userId="me", maxResults=max_results)
        .execute()
        .get("messages", [])
    )


def process_message(service, message_id: str) -> EmailData:
    """Pure processing pipeline"""
    raw_email = (
        service.users()
        .messages()
        .get(userId="me", id=message_id, format="full")
        .execute()
    )
    return parse_email(raw_email)

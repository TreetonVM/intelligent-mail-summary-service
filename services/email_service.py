from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from services.auth_service import GmailAuthenticator
from utils.email_parser import EmailParser, ParsedEmail


class GmailClient:
    """Handles Gmail API interactions"""

    def __init__(self):
        self.service = build(
            "gmail", "v1", credentials=GmailAuthenticator().get_credentials()
        )

    def fetch_emails(self, max_results: int = 10) -> list[ParsedEmail]:
        try:
            messages = self._fetch_message_list(max_results)
            return [self._process_message(msg["id"]) for msg in messages]
        except HttpError as error:
            raise EmailFetchError(f"Gmail API error: {error}")

    def _fetch_message_list(self, max_results: int) -> list[dict]:
        response = (
            self.service.users()
            .messages()
            .list(userId="me", maxResults=max_results)
            .execute()
        )
        return response.get("messages", [])

    def _process_message(self, message_id: str) -> ParsedEmail:
        raw_email = (
            self.service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )
        return EmailParser.parse_email(raw_email)


class EmailFetchError(Exception):
    """Custom exception for email fetching failures"""

    pass

import base64
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class GmailService:
    def __init__(self):
        self.creds = self._authenticate()
        self.service = build("gmail", "v1", credentials=self.creds)

    def _authenticate(self):
        creds = None
        if os.path.exists("env/token.json"):
            creds = Credentials.from_authorized_user_file("env/token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "env/client_secret.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("env/token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def fetch_emails(self, max_results: int = 10) -> list[dict]:
        try:
            # Fetch email IDs
            results = (
                self.service.users()
                .messages()
                .list(userId="me", maxResults=max_results)
                .execute()
            )
            messages = results.get("messages", [])

            emails = []
            for msg in messages:
                # Fetch full email data
                email_data = (
                    self.service.users()
                    .messages()
                    .get(userId="me", id=msg["id"], format="full")
                    .execute()
                )
                payload = email_data.get("payload", {})
                headers = payload.get("headers", [])
                parts = payload.get("parts", [])

                # Extract metadata
                sender = next(
                    (h["value"] for h in headers if h["name"] == "From"), "N/A"
                )
                subject = next(
                    (h["value"] for h in headers if h["name"] == "Subject"), "N/A"
                )
                date = next((h["value"] for h in headers if h["name"] == "Date"), "N/A")

                # Extract body (plain & HTML)
                body_plain = ""
                body_html = ""
                for part in parts:
                    if part["mimeType"] == "text/plain":
                        body_plain = base64.urlsafe_b64decode(
                            part["body"]["data"].encode("ASCII")
                        ).decode("utf-8")
                    elif part["mimeType"] == "text/html":
                        body_html = base64.urlsafe_b64decode(
                            part["body"]["data"].encode("ASCII")
                        ).decode("utf-8")

                emails.append(
                    {
                        "sender": sender,
                        "subject": subject,
                        "date": date,
                        "body_plain": body_plain,
                        "body_html": body_html,
                    }
                )

            return emails

        except HttpError as error:
            raise Exception(f"Gmail API error: {error}") from error

    def fetch_labels(self):
        try:
            results = self.service.users().labels().list(userId="me").execute()
            return results.get("labels", [])
        except HttpError as error:
            raise Exception(f"An error occurred: {error}") from error

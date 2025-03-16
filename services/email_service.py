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

    def fetch_labels(self):
        try:
            results = self.service.users().labels().list(userId="me").execute()
            return results.get("labels", [])
        except HttpError as error:
            raise Exception(f"An error occurred: {error}") from error

from pathlib import Path
from typing import cast

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class GmailAuthenticator:
    """Handles OAuth 2.0 flow and token management"""

    def __init__(self, secrets_path: Path = Path("env/client_secrets.json")):
        self.SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
        self.secrets_path = secrets_path
        self.token_path = Path("env/token.json")

    def get_credentials(self) -> Credentials:
        """Returns valid credentials, refreshing tokens if needed"""
        creds = self._load_existing_credentials()

        if not creds or not creds.valid:
            creds = self._refresh_or_create_credentials(creds)
            self._save_credentials(creds)

        return creds

    def _load_existing_credentials(self) -> Credentials | None:
        if self.token_path.exists():
            return Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        return None

    def _refresh_or_create_credentials(self, creds: Credentials | None) -> Credentials:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            return creds
        return self._create_new_credentials()

    def _create_new_credentials(self) -> Credentials:
        flow = InstalledAppFlow.from_client_secrets_file(self.secrets_path, self.SCOPES)
        # Explicitly cast to ensure type checker recognizes the correct type
        return cast(Credentials, flow.run_local_server(port=0))

    def _save_credentials(self, creds: Credentials) -> None:
        with open(self.token_path, "w") as token_file:
            token_file.write(creds.to_json())

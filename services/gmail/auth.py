from pathlib import Path
from typing import cast

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CREDENTIALS_PATH = Path("env/client_secret.json")
TOKEN_PATH = Path("env/token.json")


def ensure_credentials() -> Credentials:
    creds = load_existing_credentials()

    if not valid_credentials(creds):
        creds = handle_missing_credentials(creds)
        save_credentials(creds)

    return cast(Credentials, creds)


def load_existing_credentials() -> Credentials | None:
    if TOKEN_PATH.exists():
        return Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    return None


def valid_credentials(creds: Credentials | None) -> bool:
    return bool(creds and creds.valid)


def handle_missing_credentials(creds: Credentials | None) -> Credentials:
    """Handle credential refresh or new creation"""
    if creds and creds.expired and creds.refresh_token:
        return refresh_credentials(creds)
    return create_new_credentials()


def refresh_credentials(creds: Credentials) -> Credentials:
    creds.refresh(Request())
    return creds


def create_new_credentials() -> Credentials:
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    return cast(Credentials, flow.run_local_server(port=0))


def save_credentials(creds: Credentials) -> None:
    TOKEN_PATH.parent.mkdir(exist_ok=True)
    with TOKEN_PATH.open("w") as token:
        token.write(creds.to_json())

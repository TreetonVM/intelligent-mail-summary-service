from pathlib import Path
from typing import cast

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_credentials(
    secrets_path: Path = Path("env/client_secret.json"),
    token_path: Path = Path("env/token.json"),
) -> Credentials:
    """Pure function for credential management"""
    creds = load_existing_credentials(token_path)
    if creds is None or not valid_credentials(creds):
        return refresh_or_create_credentials(creds, secrets_path, token_path)
    else:
        return creds


def load_existing_credentials(token_path: Path) -> Credentials | None:
    """Load credentials from file without side effects"""
    return (
        Credentials.from_authorized_user_file(token_path, SCOPES)
        if token_path.exists()
        else None
    )


def valid_credentials(creds: Credentials | None) -> bool:
    """Predicate function for credential validity"""
    return bool(creds and creds.valid and not creds.expired)


def refresh_or_create_credentials(
    creds: Credentials | None, secrets_path: Path, token_path: Path
) -> Credentials:
    """Decision function for credential refresh/create flow"""
    if creds and creds.expired and creds.refresh_token:
        return refresh_credentials(creds)
    return create_new_credentials(secrets_path, token_path)


def refresh_credentials(creds: Credentials) -> Credentials:
    """Pure refresh operation"""
    creds.refresh(Request())
    return creds


def create_new_credentials(secrets_path: Path, token_path: Path) -> Credentials:
    """Pure credential creation with controlled side effect"""
    flow = InstalledAppFlow.from_client_secrets_file(secrets_path, SCOPES)
    creds = flow.run_local_server(port=0)
    save_credentials(cast(Credentials, creds), token_path)
    return cast(Credentials, creds)


def save_credentials(creds: Credentials, token_path: Path) -> None:
    """Isolated I/O operation"""
    token_path.write_text(creds.to_json())

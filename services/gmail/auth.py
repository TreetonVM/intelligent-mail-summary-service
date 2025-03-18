from typing import cast

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from config.gmail import user_gmail


def ensure_credentials() -> Credentials:
    creds = load_existing_credentials()

    if not valid_credentials(creds):
        creds = handle_missing_credentials(creds)
        save_credentials(creds)

    return cast(Credentials, creds)


def load_existing_credentials() -> Credentials | None:
    if user_gmail.TOKEN.exists():
        return Credentials.from_authorized_user_file(
            user_gmail.TOKEN, user_gmail.SCOPES
        )
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
    flow = InstalledAppFlow.from_client_secrets_file(
        user_gmail.CLIENT_SECRET, user_gmail.SCOPES
    )
    return cast(Credentials, flow.run_local_server(port=0))


def save_credentials(creds: Credentials) -> None:
    user_gmail.TOKEN.parent.mkdir(exist_ok=True)
    with user_gmail.TOKEN.open("w") as token:
        token.write(creds.to_json())

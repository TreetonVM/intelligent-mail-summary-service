# config/gmail.py
from pydantic_settings import BaseSettings


class GmailConfig(BaseSettings):
    client_secret_path: str = "env/client_secrets.json"
    token_path: str = "env/token.json"
    scopes: list[str] = ["https://www.googleapis.com/auth/gmail.readonly"]
    max_results: int = 20

    class Config:
        env_prefix = "GMAIL_"
        env_file = ".env"

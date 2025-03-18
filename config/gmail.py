from pathlib import Path

from pydantic_settings import BaseSettings


class GmailConfig(BaseSettings):
    _CLIENT_SECRET: Path = Path("env/client_secret.json")
    _TOKEN: Path = Path("env/token.json")
    _SCOPES: list[str] = ["https://www.googleapis.com/auth/gmail.readonly"]
    _MAX_RESULTS: int = 20

    @property
    def CLIENT_SECRET(self) -> Path:
        return self._CLIENT_SECRET

    @property
    def TOKEN(self) -> Path:
        return self._TOKEN

    @property
    def SCOPES(self) -> list[str]:
        return self._SCOPES

    @property
    def MAX_RESULTS(self) -> int:
        return self._MAX_RESULTS

    class Config:
        env_prefix = "GMAIL_"
        env_file = ".env"


user_gmail = GmailConfig()

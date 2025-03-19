from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings


class LogConfig(BaseSettings):
    LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    FILE: Path = Path("logs/app.log")
    MAX_SIZE: int = 10  # MB
    BACKUP_COUNT: int = 5

    class Config:
        env_prefix = "LOG_"
        env_file = ".env"


log_config = LogConfig()

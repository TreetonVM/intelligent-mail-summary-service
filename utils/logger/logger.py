import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.logging import log_config
from utils.logger.security import sanitize_log_output


def configure_root_logger() -> None:
    """Configure root logger with file and console handlers"""
    logger = logging.getLogger()
    logger.setLevel(log_config.LEVEL)

    if logger.hasHandlers():
        logger.handlers.clear()

    # Create logs directory and file if they don't exist
    log_path = Path(log_config.FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists():
        log_path.touch()
        logger.info(f"Created new log file at {log_path}")

    file_handler = RotatingFileHandler(
        filename=log_config.FILE,
        maxBytes=log_config.MAX_SIZE * 1024 * 1024,
        backupCount=log_config.BACKUP_COUNT,
    )
    file_handler.setFormatter(logging.Formatter(log_config.FORMAT))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_config.FORMAT))

    # Add security filter
    file_handler.addFilter(SecurityFilter())
    console_handler.addFilter(SecurityFilter())

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


class SecurityFilter(logging.Filter):
    """Filter sensitive information from logs"""

    def filter(self, record):
        record.msg = sanitize_log_output(str(record.msg))
        return True


def get_logger(name: str) -> logging.Logger:
    """Get configured logger instance"""
    return logging.getLogger(name)

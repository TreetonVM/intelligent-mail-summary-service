import os
import sys

# Add the parent directory to the Python path
# This allows importing modules from the parent directory (project root)
# which is necessary to import modules when running this script directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.llm.summary import create_summarizer, summarize_email
from utils.logger.logger import configure_root_logger, get_logger

configure_root_logger()
logger = get_logger("init_ollama")


def test_prompt(email_body: str, style: str = "default") -> None:
    summarizer = create_summarizer()
    logger.info(f"Testing prompt style: {style}")
    logger.info(f"Input:\n{email_body}\n")

    try:
        summary = summarize_email(email_body, summarizer)
        logger.info(f"Output:\n{summary}\n")
    except Exception as e:
        logger.error(f"Summarization failed: {e!s}")


def load_sample_email() -> str:
    return (
        "Important Meeting Reminder:\n"
        "Date: 2024-03-15 14:00\n"
        "Location: Conference Room B\n"
        "Agenda: Q2 Product Launch Planning"
    )


if __name__ == "__main__":
    email_content = sys.argv[1] if len(sys.argv) > 1 else load_sample_email()

    test_prompt(email_content, "default")
    test_prompt(email_content, "technical")

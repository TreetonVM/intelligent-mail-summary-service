import base64
from dataclasses import dataclass


@dataclass
class ParsedEmail:
    sender: str
    subject: str
    date: str
    body_plain: str
    body_html: str


class EmailParser:
    """Handles parsing of raw Gmail API responses"""

    @staticmethod
    def parse_email(raw_email: dict) -> ParsedEmail:
        headers = raw_email.get("payload", {}).get("headers", [])
        parts = raw_email.get("payload", {}).get("parts", [])

        return ParsedEmail(
            sender=EmailParser._find_header(headers, "From"),
            subject=EmailParser._find_header(headers, "Subject"),
            date=EmailParser._find_header(headers, "Date"),
            body_plain=EmailParser._extract_body(parts, "text/plain"),
            body_html=EmailParser._extract_body(parts, "text/html"),
        )

    @staticmethod
    def _find_header(headers: list[dict], name: str) -> str:
        return next((h["value"] for h in headers if h["name"] == name), "N/A")

    @staticmethod
    def _extract_body(parts: list[dict], mime_type: str) -> str:
        for part in parts:
            if part["mimeType"] == mime_type:
                data = part["body"]["data"]
                return base64.urlsafe_b64decode(data).decode("utf-8")
        return ""

import base64
from dataclasses import dataclass


@dataclass(frozen=True)
class EmailData:
    sender: str
    subject: str
    date: str
    body_plain: str
    body_html: str


def parse_email(raw: dict) -> EmailData:
    """Pure function for email parsing"""
    headers = raw.get("payload", {}).get("headers", [])
    parts = raw.get("payload", {}).get("parts", [])

    return EmailData(
        sender=extract_header(headers, "From"),
        subject=extract_header(headers, "Subject"),
        date=extract_header(headers, "Date"),
        body_plain=extract_body(parts, "text/plain"),
        body_html=extract_body(parts, "text/html"),
    )


def extract_header(headers: list[dict], name: str) -> str:
    """Pure header extraction"""
    return next((h["value"] for h in headers if h["name"] == name), "N/A")


def extract_body(parts: list[dict], mime_type: str) -> str:
    """Pure body content extraction"""
    for part in parts:
        if part["mimeType"] == mime_type:
            return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
    return ""

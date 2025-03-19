import re


def sanitize_log_output(text: str) -> str:
    """Redact sensitive information from log messages"""
    redactions = [
        (r"(Bearer\s+)\w+", r"\1[REDACTED]"),
        (
            r"(eyJ[a-zA-Z0-9_-]{5,}\.eyJ[a-zA-Z0-9_-]{5,}\.[a-zA-Z0-9_-]{10,})",
            "[JWT_REDACTED]",
        ),
        (r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", "[CARD_REDACTED]"),
    ]

    for pattern, replacement in redactions:
        text = re.sub(pattern, replacement, text)

    return text

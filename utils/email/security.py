import re


def sanitize_email_body(text: str) -> str:
    cleaned = re.sub(
        r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE
    )
    cleaned = re.sub(
        r"<iframe[^>]*>.*?</iframe>", "", cleaned, flags=re.DOTALL | re.IGNORECASE
    )

    return cleaned.strip()[:5000]

import base64


def get_email_headers(headers, target):
    return next(
        (header["value"] for header in headers if header["name"] == target), "N/A"
    )


def get_email_body(part):
    return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")


def get_email_parts(parts):
    """Extract plain and HTML bodies from email parts"""
    bodies = {"plain": "", "html": ""}
    for part in parts:
        if part["mimeType"] == "text/plain":
            bodies["plain"] = get_email_body(part)
        elif part["mimeType"] == "text/html":
            bodies["html"] = get_email_body(part)
    return bodies

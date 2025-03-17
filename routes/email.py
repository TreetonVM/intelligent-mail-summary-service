from fastapi import APIRouter, HTTPException, Query

from schemas.email import SummarizedEmail
from services.email_service import (
    create_gmail_service,
    fetch_email_metadata,
    get_email_details,
    parse_email_headers,
    process_email_parts,
)
from services.llm import create_summarizer, summarize_email

router = APIRouter(tags=["Gmail"])


@router.get("/emails")
def get_emails(max_results: int = Query(default=5, ge=1, le=20)):
    """Fetch recent emails with metadata and content"""
    try:
        service = create_gmail_service()
        messages = fetch_email_metadata(service, max_results)

        emails = []
        for message in messages:
            email_data = get_email_details(service, message["id"])
            payload = email_data.get("payload", {})

            headers = payload.get("headers", [])
            parts = payload.get("parts", [])

            bodies = process_email_parts(parts)

            emails.append(
                {
                    "sender": parse_email_headers(headers, "From"),
                    "subject": parse_email_headers(headers, "Subject"),
                    "date": parse_email_headers(headers, "Date"),
                    "body_plain": bodies["plain"],
                    "body_html": bodies["html"],
                }
            )

        return emails

    except Exception as exception_message:
        raise HTTPException(
            status_code=503, detail=f"Email service error: {exception_message!s}"
        ) from exception_message


summarizer = create_summarizer()


@router.get("/emails/summarized", response_model=list[SummarizedEmail])
def get_summarized_emails(max_results: int = 3):
    try:
        emails = get_emails(max_results)
        return [
            {**email, "summary": summarize_email(email["body_plain"], summarizer)}
            for email in emails
        ]
    except Exception as e:
        raise HTTPException(500, f"Summarization failed: {e!s}") from e

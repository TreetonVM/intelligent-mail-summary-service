from fastapi import APIRouter, HTTPException, Query

from schemas.email_summary import EmailSummary
from schemas.original_email import OriginalEmail
from services.gmail.inbox import (
    create_gmail_service,
    fetch_email_details,
    fetch_email_metadata,
)
from services.gmail.utils import get_email_headers, get_email_parts
from services.llm.summary import create_summarizer, summarize_email

router = APIRouter(tags=["Gmail"])


@router.get("/emails", response_model=list[OriginalEmail])
def get_emails(
    max_results: int = Query(default=5, ge=1, le=20),
) -> list[OriginalEmail]:
    try:
        service = create_gmail_service()
        recent_messages = fetch_email_metadata(service, max_results)

        emails = []
        for message in recent_messages:
            email_details = fetch_email_details(service, message["id"])
            payload = email_details.get("payload", {})

            headers = payload.get("headers", [])
            parts = payload.get("parts", [])

            email_bodies = get_email_parts(parts)

            emails.append(
                {
                    "sender": get_email_headers(headers, "From"),
                    "subject": get_email_headers(headers, "Subject"),
                    "date": get_email_headers(headers, "Date"),
                    "body_plain": email_bodies["plain"],
                    "body_html": email_bodies["html"],
                }
            )

        return [OriginalEmail(**email) for email in emails]

    except Exception as exc:
        raise HTTPException(
            status_code=503, detail=f"Email service error: {exc!s}"
        ) from exc


@router.get("/emails/summarized", response_model=list[EmailSummary])
def get_summarized_emails(max_results: int = 3):
    summarizer = create_summarizer()

    try:
        emails = get_emails(max_results)
        return [
            {
                **email.model_dump(),
                "summary": summarize_email(email.body_plain or "", summarizer),
            }
            for email in emails
        ]
    except Exception as exc:
        raise HTTPException(500, f"Summarization failed: {exc!s}") from exc

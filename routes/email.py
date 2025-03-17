from fastapi import APIRouter, HTTPException, Query

from schemas.email import Email, SummarizedEmail
from services.email_service import (
    create_gmail_service,
    fetch_email_metadata,
    get_email_details,
    parse_email_headers,
    process_email_parts,
)
from services.llm import create_summarizer, summarize_email

router = APIRouter(tags=["Gmail"])


@router.get("/emails", response_model=list[Email])
def get_emails(
    max_results: int = Query(default=5, ge=1, le=20),
) -> list[Email]:
    try:
        service = create_gmail_service()
        recent_messages = fetch_email_metadata(service, max_results)

        emails = []
        for message in recent_messages:
            email_details = get_email_details(service, message["id"])
            payload = email_details.get("payload", {})

            headers = payload.get("headers", [])
            parts = payload.get("parts", [])

            email_bodies = process_email_parts(parts)

            emails.append(
                {
                    "sender": parse_email_headers(headers, "From"),
                    "subject": parse_email_headers(headers, "Subject"),
                    "date": parse_email_headers(headers, "Date"),
                    "body_plain": email_bodies["plain"],
                    "body_html": email_bodies["html"],
                }
            )

        return [Email(**email) for email in emails]

    except Exception as exc:
        raise HTTPException(
            status_code=503, detail=f"Email service error: {exc!s}"
        ) from exc


summarizer = create_summarizer()


@router.get("/emails/summarized", response_model=list[SummarizedEmail])
def get_summarized_emails(max_results: int = 3):
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

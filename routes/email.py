from fastapi import APIRouter, HTTPException, Query

from schemas.email import EmailSummary
from services.email_service import EmailFetchError, GmailClient

router = APIRouter(tags=["Gmail"])


@router.get("/emails", response_model=list[EmailSummary])
async def get_recent_emails(
    max_results: int = Query(
        default=5, ge=1, le=20, description="Number of emails to fetch"
    ),
):
    """Fetch recent emails with metadata and body content"""
    try:
        return GmailClient().fetch_emails(max_results)
    except EmailFetchError as e:
        raise HTTPException(status_code=503, detail=f"Email service unavailable: {e!s}")

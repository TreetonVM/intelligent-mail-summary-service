from fastapi import APIRouter, HTTPException

from schemas.email import EmailSummary
from services.email_service import GmailService

router = APIRouter()


@router.get("/emails", response_model=list[EmailSummary], tags=["Gmail"])
def get_emails(max_results: int = 5):
    try:
        service = GmailService()
        emails = service.fetch_emails(max_results)
        return emails
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch emails: {e!s}"
        ) from e

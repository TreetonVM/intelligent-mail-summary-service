from fastapi import APIRouter, HTTPException, Query

from services.email import create_gmail_service, fetch_emails
from utils.parsing import EmailData

router = APIRouter(tags=["Gmail"])


@router.get("/emails", response_model=list[EmailData])
def get_emails(max_results: int = Query(default=5, ge=1, le=20)):
    """Endpoint composed from pure functions"""
    service = create_gmail_service()
    emails, error = fetch_emails(service, max_results)

    if error:
        raise HTTPException(status_code=503, detail=f"Gmail service error: {error!s}")

    return emails

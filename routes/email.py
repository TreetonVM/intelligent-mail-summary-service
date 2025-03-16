from fastapi import APIRouter, HTTPException

from services.email_service import GmailService

router = APIRouter()


@router.get("/emails/labels", tags=["Gmail"])
def get_email_labels():
    try:
        service = GmailService()
        labels = service.fetch_labels()
        return {"labels": labels}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

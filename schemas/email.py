from typing import ClassVar

from pydantic import BaseModel, Field


class EmailSummary(BaseModel):
    sender: str
    subject: str
    date: str
    body_plain: str | None = None
    body_html: str | None = None

    class Config:
        json_schema_extra: ClassVar[dict] = {
            "example": {
                "sender": "John Doe <john@example.com>",
                "subject": "Meeting Tomorrow",
                "date": "Wed, 15 Mar 2023 14:30:00 +0000",
                "body_plain": "Please confirm your attendance...",
                "body_html": "<p>Please confirm your attendance...</p>",
            }
        }


class SummarizedEmail(BaseModel):
    sender: str
    subject: str
    date: str
    summary: str
    body_preview: str = Field(..., alias="body_plain")

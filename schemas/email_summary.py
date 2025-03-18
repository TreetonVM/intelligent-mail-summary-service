from pydantic import BaseModel


class EmailSummary(BaseModel):
    sender: str
    subject: str
    date: str
    summary: str

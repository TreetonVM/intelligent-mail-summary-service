from pydantic import BaseModel


class EmailSummary(BaseModel):
    sender: str
    subject: str
    date: str
    body_plain: str
    body_html: str

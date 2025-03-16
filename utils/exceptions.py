from fastapi import HTTPException


class GmailException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=503, detail=f"Gmail service error: {detail}")

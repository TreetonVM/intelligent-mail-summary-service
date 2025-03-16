from fastapi import FastAPI

from routes import email

app = FastAPI()
app.include_router(email.router)

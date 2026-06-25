from fastapi import FastAPI
from app.core.database import engine
from sqlalchemy import text
from app.api import repos

app = FastAPI(
    title = "DevPulse",
    description = "Developer activity & productivity tracking",
    version = "0.1.0"
)
app.include_router(repos.router)

@app.get("/")
def root():
    return {"message": "DevPulse API is running!"}

@app.get("/health")
def health_check():
    return {"status": "okay"}

@app.get("/db-check")
def db_check():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"database": "connected"}
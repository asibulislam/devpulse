from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.database import engine
from sqlalchemy import text
from app.api import repos, analytics, auth

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="DevPulse",
    description="Developer activity & productivity tracking",
    version="0.1.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "detail": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


app.include_router(repos.router)
app.include_router(analytics.router)
app.include_router(auth.router)


@app.get("/", summary="Root — confirm the API is running")
def root():
    return {"message": "DevPulse API is running!"}


@app.get("/health", summary="Health check")
def health_check():
    return {"status": "okay"}


@app.get("/db-check", summary="Database connection check")
def db_check():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"database": "connected"}
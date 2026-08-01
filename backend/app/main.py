import logging
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings
from app.database import SessionLocal
from app.modules.dashboard.router import router as dashboard_router
from app.modules.documents.router import router as documents_router
from app.modules.identity.router import router as identity_router
from app.modules.translation.router import router as translation_router
from app.platform.errors import AppError, install_error_handlers

settings = get_settings()
logging.basicConfig(
    level=settings.AIKYA_LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(
    title="Aikya AI API",
    version="0.1.0",
    docs_url="/api/docs" if settings.AIKYA_ENV != "production" else None,
    redoc_url=None,
    openapi_url="/api/openapi.json" if settings.AIKYA_ENV != "production" else None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Idempotency-Key", "If-Match"],
)


@app.middleware("http")
async def request_context(request: Request, call_next):  # type: ignore[no-untyped-def]
    request.state.request_id = str(uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response


@app.get("/health/live", tags=["health"])
def live() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready", tags=["health"])
def ready() -> dict[str, str]:
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise AppError(
            "database_not_ready",
            "The service is not ready.",
            status_code=503,
            retryable=True,
        ) from exc
    return {"status": "ready"}


app.include_router(identity_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(translation_router, prefix="/api/v1")
app.include_router(documents_router, prefix="/api/v1")
install_error_handlers(app)

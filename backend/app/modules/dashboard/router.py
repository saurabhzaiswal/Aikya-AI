from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.modules.documents.models import Document
from app.modules.documents.service import list_documents
from app.modules.identity.dependencies import CurrentPrincipal, get_current_principal
from app.modules.translation.models import TextTranslation
from app.modules.translation.service import list_history

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def dashboard_summary(
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    document_count = (
        db.scalar(
            select(func.count(Document.id)).where(
                Document.organization_id == principal.organization_id
            )
        )
        or 0
    )
    translation_count = (
        db.scalar(
            select(func.count(TextTranslation.id)).where(
                TextTranslation.organization_id == principal.organization_id
            )
        )
        or 0
    )
    settings = get_settings()
    return {
        "document_count": document_count,
        "text_translation_count": translation_count,
        "recent_documents": list_documents(db, principal.organization_id, limit=5),
        "recent_translations": list_history(db, principal.organization_id, limit=5),
        "limits": {
            "max_upload_bytes": settings.MAX_UPLOAD_BYTES,
            "max_document_pages": settings.MAX_DOCUMENT_PAGES,
            "max_text_characters": settings.MAX_TEXT_TRANSLATION_CHARACTERS,
        },
    }

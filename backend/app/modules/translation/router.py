from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.modules.identity.dependencies import CurrentPrincipal, get_current_principal
from app.modules.translation.schemas import (
    LanguageResponse,
    TextTranslationRequest,
    TextTranslationResponse,
    TranslationHistoryResponse,
)
from app.modules.translation.service import list_history, translate_text
from app.platform.rate_limit import check_rate_limit

router = APIRouter(prefix="/translation", tags=["translation"])
settings = get_settings()

LANGUAGES = [
    LanguageResponse(code="en", name="English"),
    LanguageResponse(code="hi", name="Hindi"),
    LanguageResponse(code="es", name="Spanish"),
    LanguageResponse(code="fr", name="French"),
    LanguageResponse(code="de", name="German"),
    LanguageResponse(code="ja", name="Japanese"),
    LanguageResponse(code="ar", name="Arabic", direction="rtl"),
]


@router.get("/languages", response_model=list[LanguageResponse])
def languages(_: CurrentPrincipal = Depends(get_current_principal)) -> list[LanguageResponse]:
    return LANGUAGES


@router.post("/text", response_model=TextTranslationResponse, status_code=201)
def create_text_translation(
    payload: TextTranslationRequest,
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> TextTranslationResponse:
    check_rate_limit(
        "text-translation",
        str(principal.user.id),
        limit=settings.TRANSLATION_RATE_LIMIT,
        window_seconds=settings.WORKLOAD_RATE_WINDOW_SECONDS,
    )
    return translate_text(
        db,
        organization_id=principal.organization_id,
        user_id=principal.user.id,
        text=payload.text,
        source_language=payload.source_language,
        target_language=payload.target_language,
    )


@router.get("/history", response_model=TranslationHistoryResponse)
def history(
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> TranslationHistoryResponse:
    return TranslationHistoryResponse(items=list_history(db, principal.organization_id))

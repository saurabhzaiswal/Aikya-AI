from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.modules.translation.models import TextTranslation
from app.modules.translation.provider import get_translation_provider
from app.modules.translation.schemas import TextTranslationResponse
from app.platform.errors import AppError


def translate_text(
    db: Session,
    *,
    organization_id: UUID,
    user_id: UUID,
    text: str,
    source_language: str,
    target_language: str,
) -> TextTranslationResponse:
    settings = get_settings()
    if len(text) > settings.MAX_TEXT_TRANSLATION_CHARACTERS:
        raise AppError(
            "translation_input_too_large",
            f"Text translation is limited to {settings.MAX_TEXT_TRANSLATION_CHARACTERS} characters.",
            status_code=413,
        )
    if source_language == target_language:
        raise AppError(
            "translation_pair_invalid",
            "Source and target languages must be different.",
            status_code=422,
        )
    provider = get_translation_provider()
    result = provider.translate(text.strip(), source_language, target_language)
    record = TextTranslation(
        organization_id=organization_id,
        created_by=user_id,
        source_language=source_language,
        detected_language=result.detected_language,
        target_language=target_language,
        source_text=text.strip(),
        translated_text=result.translated_text,
        provider=provider.name,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return to_response(record)


def list_history(
    db: Session, organization_id: UUID, limit: int = 20
) -> list[TextTranslationResponse]:
    rows = db.scalars(
        select(TextTranslation)
        .where(TextTranslation.organization_id == organization_id)
        .order_by(TextTranslation.created_at.desc(), TextTranslation.id.desc())
        .limit(limit)
    ).all()
    return [to_response(row) for row in rows]


def to_response(record: TextTranslation) -> TextTranslationResponse:
    return TextTranslationResponse(
        id=record.id,
        source_language=record.source_language,
        detected_language=record.detected_language,
        target_language=record.target_language,
        source_text=record.source_text,
        translated_text=record.translated_text,
        created_at=record.created_at,
    )

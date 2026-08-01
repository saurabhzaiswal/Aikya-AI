from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class LanguageResponse(BaseModel):
    code: str
    name: str
    direction: str = "ltr"


class TextTranslationRequest(BaseModel):
    text: str = Field(min_length=1)
    source_language: str = Field(default="auto", min_length=2, max_length=35)
    target_language: str = Field(min_length=2, max_length=35)

    @field_validator("text")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Text cannot be blank")
        return value


class TextTranslationResponse(BaseModel):
    id: UUID
    source_language: str
    detected_language: str | None
    target_language: str
    source_text: str
    translated_text: str
    created_at: datetime


class TranslationHistoryResponse(BaseModel):
    items: list[TextTranslationResponse]

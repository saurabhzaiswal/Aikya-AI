from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.platform.identifiers import new_uuid7


def utc_now() -> datetime:
    return datetime.now(UTC)


class TextTranslation(Base):
    __tablename__ = "text_translations"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=new_uuid7)
    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    source_language: Mapped[str] = mapped_column(String(35), default="auto")
    detected_language: Mapped[str | None] = mapped_column(String(35), nullable=True)
    target_language: Mapped[str] = mapped_column(String(35))
    source_text: Mapped[str] = mapped_column(Text)
    translated_text: Mapped[str] = mapped_column(Text)
    provider: Mapped[str] = mapped_column(String(60))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, index=True
    )

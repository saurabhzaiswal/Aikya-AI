from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.platform.identifiers import new_uuid7


def utc_now() -> datetime:
    return datetime.now(UTC)


class FileObject(Base):
    __tablename__ = "file_objects"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=new_uuid7)
    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    purpose: Mapped[str] = mapped_column(String(30))
    bucket: Mapped[str] = mapped_column(String(120))
    object_key: Mapped[str] = mapped_column(String(500), unique=True)
    display_name: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(120))
    expected_size: Mapped[int] = mapped_column(BigInteger)
    actual_size: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    expected_checksum: Mapped[str] = mapped_column(String(64))
    actual_checksum: Mapped[str | None] = mapped_column(String(64), nullable=True)
    lifecycle_status: Mapped[str] = mapped_column(String(30), default="pending_upload", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=new_uuid7)
    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    workspace_id: Mapped[UUID] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"))
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    source_file_id: Mapped[UUID] = mapped_column(
        ForeignKey("file_objects.id", ondelete="RESTRICT"), unique=True
    )
    title: Mapped[str] = mapped_column(String(255))
    source_language: Mapped[str] = mapped_column(String(35), default="auto")
    status: Mapped[str] = mapped_column(String(30), default="uploaded", index=True)
    page_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    warning_code: Mapped[str | None] = mapped_column(String(80), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )


class ProcessingJob(Base):
    __tablename__ = "processing_jobs"
    __table_args__ = (UniqueConstraint("organization_id", "idempotency_key"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=new_uuid7)
    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), index=True
    )
    requested_by: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    target_language: Mapped[str] = mapped_column(String(35))
    state: Mapped[str] = mapped_column(String(30), default="queued", index=True)
    stage: Mapped[str] = mapped_column(String(30), default="queued")
    progress: Mapped[int] = mapped_column(Integer, default=0)
    idempotency_key: Mapped[str] = mapped_column(String(120))
    output_file_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("file_objects.id", ondelete="SET NULL"), nullable=True
    )
    error_code: Mapped[str | None] = mapped_column(String(80), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, index=True
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

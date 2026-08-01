from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.platform.identifiers import new_uuid7


def utc_now() -> datetime:
    return datetime.now(UTC)


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=new_uuid7)
    name: Mapped[str] = mapped_column(String(160))
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    kind: Mapped[str] = mapped_column(String(20), default="personal")
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class OrganizationMembership(Base):
    __tablename__ = "organization_memberships"
    __table_args__ = (UniqueConstraint("organization_id", "user_id"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=new_uuid7)
    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    role: Mapped[str] = mapped_column(String(20), default="owner")
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=new_uuid7)
    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(160), default="My Workspace")
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

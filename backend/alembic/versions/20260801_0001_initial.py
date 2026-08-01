"""Create Phase 1 identity, tenancy, translation, document, and job tables.

Revision ID: 20260801_0001
Revises: None
Create Date: 2026-08-01
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260801_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def timestamps() -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    ]


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=512), nullable=False),
        sa.Column("locale", sa.String(length=35), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "organizations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("slug", sa.String(length=180), nullable=False),
        sa.Column("kind", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index("ix_organizations_slug", "organizations", ["slug"])

    op.create_table(
        "organization_memberships",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "user_id"),
    )
    op.create_index(
        "ix_organization_memberships_organization_id",
        "organization_memberships",
        ["organization_id"],
    )
    op.create_index("ix_organization_memberships_user_id", "organization_memberships", ["user_id"])

    op.create_table(
        "workspaces",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workspaces_organization_id", "workspaces", ["organization_id"])

    op.create_table(
        "sessions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("refresh_token_hash", sa.String(length=64), nullable=False),
        sa.Column("family_id", sa.Uuid(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("replaced_by_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["replaced_by_id"], ["sessions.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("refresh_token_hash"),
    )
    op.create_index("ix_sessions_user_id", "sessions", ["user_id"])
    op.create_index("ix_sessions_family_id", "sessions", ["family_id"])
    op.create_index("ix_sessions_refresh_token_hash", "sessions", ["refresh_token_hash"])

    op.create_table(
        "file_objects",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=False),
        sa.Column("purpose", sa.String(length=30), nullable=False),
        sa.Column("bucket", sa.String(length=120), nullable=False),
        sa.Column("object_key", sa.String(length=500), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("content_type", sa.String(length=120), nullable=False),
        sa.Column("expected_size", sa.BigInteger(), nullable=False),
        sa.Column("actual_size", sa.BigInteger(), nullable=True),
        sa.Column("expected_checksum", sa.String(length=64), nullable=False),
        sa.Column("actual_checksum", sa.String(length=64), nullable=True),
        sa.Column("lifecycle_status", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("object_key"),
    )
    op.create_index("ix_file_objects_organization_id", "file_objects", ["organization_id"])
    op.create_index("ix_file_objects_lifecycle_status", "file_objects", ["lifecycle_status"])
    op.create_index("ix_file_objects_expires_at", "file_objects", ["expires_at"])

    op.create_table(
        "documents",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("workspace_id", sa.Uuid(), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=False),
        sa.Column("source_file_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("source_language", sa.String(length=35), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("page_count", sa.Integer(), nullable=True),
        sa.Column("warning_code", sa.String(length=80), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_file_id"], ["file_objects.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_file_id"),
    )
    op.create_index("ix_documents_organization_id", "documents", ["organization_id"])
    op.create_index("ix_documents_status", "documents", ["status"])
    op.create_index("ix_documents_created_at", "documents", ["created_at"])

    op.create_table(
        "text_translations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("created_by", sa.Uuid(), nullable=False),
        sa.Column("source_language", sa.String(length=35), nullable=False),
        sa.Column("detected_language", sa.String(length=35), nullable=True),
        sa.Column("target_language", sa.String(length=35), nullable=False),
        sa.Column("source_text", sa.Text(), nullable=False),
        sa.Column("translated_text", sa.Text(), nullable=False),
        sa.Column("provider", sa.String(length=60), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_text_translations_organization_id", "text_translations", ["organization_id"]
    )
    op.create_index("ix_text_translations_created_at", "text_translations", ["created_at"])

    op.create_table(
        "processing_jobs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("document_id", sa.Uuid(), nullable=False),
        sa.Column("requested_by", sa.Uuid(), nullable=False),
        sa.Column("target_language", sa.String(length=35), nullable=False),
        sa.Column("state", sa.String(length=30), nullable=False),
        sa.Column("stage", sa.String(length=30), nullable=False),
        sa.Column("progress", sa.Integer(), nullable=False),
        sa.Column("idempotency_key", sa.String(length=120), nullable=False),
        sa.Column("output_file_id", sa.Uuid(), nullable=True),
        sa.Column("error_code", sa.String(length=80), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["output_file_id"], ["file_objects.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["requested_by"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "idempotency_key"),
    )
    op.create_index("ix_processing_jobs_organization_id", "processing_jobs", ["organization_id"])
    op.create_index("ix_processing_jobs_document_id", "processing_jobs", ["document_id"])
    op.create_index("ix_processing_jobs_state", "processing_jobs", ["state"])
    op.create_index("ix_processing_jobs_created_at", "processing_jobs", ["created_at"])


def downgrade() -> None:
    op.drop_table("processing_jobs")
    op.drop_table("text_translations")
    op.drop_table("documents")
    op.drop_table("file_objects")
    op.drop_table("sessions")
    op.drop_table("workspaces")
    op.drop_table("organization_memberships")
    op.drop_table("organizations")
    op.drop_table("users")

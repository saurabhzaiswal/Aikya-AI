"""Import all SQLAlchemy models so Alembic sees one metadata graph."""

from app.modules.documents.models import Document, FileObject, ProcessingJob
from app.modules.identity.models import (
    ExternalIdentity,
    RecoveryCode,
    SessionRecord,
    User,
    WebAuthnChallenge,
    WebAuthnCredential,
)
from app.modules.organizations.models import Organization, OrganizationMembership, Workspace
from app.modules.translation.models import TextTranslation

__all__ = [
    "Document",
    "ExternalIdentity",
    "FileObject",
    "Organization",
    "OrganizationMembership",
    "ProcessingJob",
    "RecoveryCode",
    "SessionRecord",
    "TextTranslation",
    "User",
    "WebAuthnChallenge",
    "WebAuthnCredential",
    "Workspace",
]

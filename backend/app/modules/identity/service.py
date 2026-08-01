import re
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.modules.identity.models import SessionRecord, User
from app.modules.identity.schemas import AuthResponse, ContextResponse, MeResponse, UserResponse
from app.modules.organizations.models import Organization, OrganizationMembership, Workspace
from app.platform.errors import AppError
from app.platform.identifiers import new_uuid7
from app.platform.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalized_utc(value: datetime) -> datetime:
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def make_slug(display_name: str) -> str:
    stem = re.sub(r"[^a-z0-9]+", "-", display_name.lower()).strip("-") or "workspace"
    return f"{stem}-{str(new_uuid7())[:8]}"


def _build_auth_response(
    user: User, organization: Organization, workspace: Workspace
) -> AuthResponse:
    settings = get_settings()
    return AuthResponse(
        access_token=create_access_token(user.id, organization.id),
        expires_in=settings.AUTH_ACCESS_TOKEN_TTL_SECONDS,
        user=UserResponse.model_validate(user),
        context=ContextResponse(
            organization_id=organization.id,
            organization_name=organization.name,
            workspace_id=workspace.id,
            workspace_name=workspace.name,
        ),
    )


def _create_session(
    db: Session, user_id: UUID, family_id: UUID | None = None
) -> tuple[str, SessionRecord]:
    settings = get_settings()
    raw_token = create_refresh_token()
    record = SessionRecord(
        user_id=user_id,
        refresh_token_hash=hash_refresh_token(raw_token),
        family_id=family_id or new_uuid7(),
        expires_at=datetime.now(UTC) + timedelta(seconds=settings.AUTH_REFRESH_TOKEN_TTL_SECONDS),
    )
    db.add(record)
    db.flush()
    return raw_token, record


def register(db: Session, email: str, password: str, display_name: str) -> tuple[AuthResponse, str]:
    normalized_email = normalize_email(email)
    if db.scalar(select(User.id).where(User.email == normalized_email)) is not None:
        raise AppError(
            "email_unavailable", "An account cannot be created with this email.", status_code=409
        )

    user = User(
        email=normalized_email,
        display_name=display_name.strip(),
        password_hash=hash_password(password),
    )
    organization = Organization(
        name=f"{display_name.strip()}'s Workspace", slug=make_slug(display_name)
    )
    try:
        db.add_all([user, organization])
        db.flush()
        membership = OrganizationMembership(
            organization_id=organization.id, user_id=user.id, role="owner"
        )
        workspace = Workspace(
            organization_id=organization.id, name="My Workspace", created_by=user.id
        )
        db.add_all([membership, workspace])
        db.flush()
        refresh_token, _ = _create_session(db, user.id)
        response = _build_auth_response(user, organization, workspace)
        db.commit()
        return response, refresh_token
    except IntegrityError as exc:
        db.rollback()
        raise AppError(
            "email_unavailable", "An account cannot be created with this email.", status_code=409
        ) from exc


def login(db: Session, email: str, password: str) -> tuple[AuthResponse, str]:
    user = db.scalar(select(User).where(User.email == normalize_email(email)))
    if user is None or not user.is_active or not verify_password(password, user.password_hash):
        raise AppError("invalid_credentials", "Email or password is incorrect.", status_code=401)
    membership = db.scalar(
        select(OrganizationMembership).where(
            OrganizationMembership.user_id == user.id,
            OrganizationMembership.status == "active",
        )
    )
    if membership is None:
        raise AppError("account_unavailable", "This account is not available.", status_code=403)
    organization = db.get(Organization, membership.organization_id)
    workspace = db.scalar(
        select(Workspace).where(Workspace.organization_id == membership.organization_id)
    )
    if organization is None or workspace is None:
        raise AppError("account_unavailable", "This account is not available.", status_code=403)
    refresh_token, _ = _create_session(db, user.id)
    response = _build_auth_response(user, organization, workspace)
    db.commit()
    return response, refresh_token


def refresh(db: Session, raw_token: str) -> tuple[AuthResponse, str]:
    now = datetime.now(UTC)
    record = db.scalar(
        select(SessionRecord)
        .where(SessionRecord.refresh_token_hash == hash_refresh_token(raw_token))
        .with_for_update()
    )
    if record is not None and record.revoked_at is not None:
        db.execute(
            update(SessionRecord)
            .where(SessionRecord.family_id == record.family_id, SessionRecord.revoked_at.is_(None))
            .values(revoked_at=now)
        )
        db.commit()
        raise AppError("invalid_refresh_token", "The session has expired.", status_code=401)
    if record is None or normalized_utc(record.expires_at) <= now:
        raise AppError("invalid_refresh_token", "The session has expired.", status_code=401)
    user = db.get(User, record.user_id)
    membership = db.scalar(
        select(OrganizationMembership).where(
            OrganizationMembership.user_id == record.user_id,
            OrganizationMembership.status == "active",
        )
    )
    if user is None or membership is None or not user.is_active:
        raise AppError("invalid_refresh_token", "The session has expired.", status_code=401)
    organization = db.get(Organization, membership.organization_id)
    workspace = db.scalar(
        select(Workspace).where(Workspace.organization_id == membership.organization_id)
    )
    if organization is None or workspace is None:
        raise AppError("invalid_refresh_token", "The session has expired.", status_code=401)
    new_raw_token, new_record = _create_session(db, user.id, record.family_id)
    record.revoked_at = now
    record.replaced_by_id = new_record.id
    response = _build_auth_response(user, organization, workspace)
    db.commit()
    return response, new_raw_token


def logout(db: Session, raw_token: str | None) -> None:
    if not raw_token:
        return
    record = db.scalar(
        select(SessionRecord).where(
            SessionRecord.refresh_token_hash == hash_refresh_token(raw_token)
        )
    )
    if record is not None and record.revoked_at is None:
        record.revoked_at = datetime.now(UTC)
        db.commit()


def get_me(db: Session, user: User, organization_id: UUID) -> MeResponse:
    organization = db.get(Organization, organization_id)
    workspace = db.scalar(select(Workspace).where(Workspace.organization_id == organization_id))
    if organization is None or workspace is None:
        raise AppError("account_unavailable", "This account is not available.", status_code=403)
    return MeResponse(
        user=UserResponse.model_validate(user),
        context=ContextResponse(
            organization_id=organization.id,
            organization_name=organization.name,
            workspace_id=workspace.id,
            workspace_name=workspace.name,
        ),
    )

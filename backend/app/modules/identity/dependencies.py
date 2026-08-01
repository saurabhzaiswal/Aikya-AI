from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.identity.models import User
from app.modules.organizations.models import OrganizationMembership
from app.platform.errors import AppError
from app.platform.security import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class CurrentPrincipal:
    user: User
    organization_id: UUID


def get_current_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> CurrentPrincipal:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AppError("authentication_required", "Authentication is required.", status_code=401)
    user_id, organization_id = decode_access_token(credentials.credentials)
    user = db.get(User, user_id)
    membership = db.scalar(
        select(OrganizationMembership).where(
            OrganizationMembership.user_id == user_id,
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.status == "active",
        )
    )
    if user is None or not user.is_active or membership is None:
        raise AppError("authentication_required", "Authentication is required.", status_code=401)
    return CurrentPrincipal(user=user, organization_id=organization_id)

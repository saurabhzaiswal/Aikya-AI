import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

from app.config import get_settings
from app.platform.errors import AppError

password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except (VerifyMismatchError, InvalidHashError):
        return False


def create_access_token(user_id: UUID, organization_id: UUID) -> str:
    settings = get_settings()
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "org": str(organization_id),
        "iss": settings.AUTH_ISSUER,
        "aud": settings.AUTH_AUDIENCE,
        "iat": now,
        "exp": now + timedelta(seconds=settings.AUTH_ACCESS_TOKEN_TTL_SECONDS),
        "jti": str(uuid4()),
        "type": "access",
    }
    return jwt.encode(payload, settings.AUTH_SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> tuple[UUID, UUID]:
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.AUTH_SECRET_KEY,
            algorithms=["HS256"],
            issuer=settings.AUTH_ISSUER,
            audience=settings.AUTH_AUDIENCE,
        )
        if payload.get("type") != "access":
            raise jwt.InvalidTokenError("Wrong token type")
        return UUID(payload["sub"]), UUID(payload["org"])
    except (jwt.PyJWTError, KeyError, ValueError) as exc:
        raise AppError(
            "invalid_access_token", "Authentication is required.", status_code=401
        ) from exc


def create_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

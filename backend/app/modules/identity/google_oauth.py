import base64
import hashlib
import hmac
import re
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import cast
from urllib.parse import urlencode
from uuid import UUID

import httpx
import jwt
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.modules.identity.models import ExternalIdentity, User
from app.modules.identity.service import (
    create_personal_account,
    load_account_context,
    normalize_email,
)
from app.modules.organizations.models import Organization, Workspace
from app.platform.errors import AppError

settings = get_settings()
GOOGLE_AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_JWKS_ENDPOINT = "https://www.googleapis.com/oauth2/v3/certs"
GOOGLE_ISSUERS = {"accounts.google.com", "https://accounts.google.com"}
STATE_AUDIENCE = "aikya-google-oauth-state"
MFA_AUDIENCE = "aikya-google-oauth-mfa"


@dataclass(frozen=True)
class GoogleAuthorization:
    url: str
    cookie: str


@dataclass(frozen=True)
class GoogleClaims:
    subject: str
    email: str
    display_name: str


def is_configured() -> bool:
    return bool(settings.AUTH_GOOGLE_CLIENT_ID and settings.AUTH_GOOGLE_CLIENT_SECRET)


def safe_return_to(value: str | None) -> str:
    if not value or not value.startswith("/") or value.startswith("//"):
        return "/app/dashboard"
    path = value.split("?", 1)[0]
    segments = [segment for segment in path.split("/") if segment]
    if segments and segments[0] == "app":
        return value
    if len(segments) >= 2 and segments[1] == "app" and len(segments[0]) <= 12:
        return value
    return "/app/dashboard"


def _b64url(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def create_authorization(return_to: str | None, locale: str | None) -> GoogleAuthorization:
    if not is_configured():
        raise AppError(
            "google_oauth_not_configured",
            "Google sign-in has not been configured yet.",
            status_code=503,
        )
    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)
    challenge = _b64url(hashlib.sha256(verifier.encode("ascii")).digest())
    safe_locale = (
        locale.lower()
        if locale and re.fullmatch(r"[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*", locale)
        else "en"
    )
    now = datetime.now(UTC)
    state_cookie = jwt.encode(
        {
            "iss": settings.AUTH_ISSUER,
            "aud": STATE_AUDIENCE,
            "iat": now,
            "exp": now + timedelta(seconds=settings.AUTH_OAUTH_STATE_TTL_SECONDS),
            "jti": secrets.token_urlsafe(18),
            "state": state,
            "nonce": nonce,
            "verifier": verifier,
            "return_to": safe_return_to(return_to),
            "locale": safe_locale,
        },
        settings.AUTH_SECRET_KEY,
        algorithm="HS256",
    )
    query = urlencode(
        {
            "client_id": settings.AUTH_GOOGLE_CLIENT_ID,
            "redirect_uri": settings.AUTH_GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "nonce": nonce,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "prompt": "select_account",
        }
    )
    return GoogleAuthorization(
        url=f"{GOOGLE_AUTHORIZATION_ENDPOINT}?{query}",
        cookie=state_cookie,
    )


def decode_state(cookie: str, received_state: str) -> dict[str, str]:
    try:
        payload = jwt.decode(
            cookie,
            settings.AUTH_SECRET_KEY,
            algorithms=["HS256"],
            audience=STATE_AUDIENCE,
            issuer=settings.AUTH_ISSUER,
        )
    except jwt.PyJWTError as exc:
        raise AppError(
            "invalid_oauth_state", "Google sign-in expired. Please try again.", status_code=400
        ) from exc
    state = payload.get("state")
    if not isinstance(state, str) or not hmac.compare_digest(state, received_state):
        raise AppError(
            "invalid_oauth_state", "Google sign-in expired. Please try again.", status_code=400
        )
    required = ("nonce", "verifier", "return_to", "locale")
    if any(not isinstance(payload.get(key), str) for key in required):
        raise AppError(
            "invalid_oauth_state", "Google sign-in expired. Please try again.", status_code=400
        )
    return {key: cast(str, payload[key]) for key in required}


def create_mfa_ticket(challenge_id: UUID) -> str:
    now = datetime.now(UTC)
    return jwt.encode(
        {
            "iss": settings.AUTH_ISSUER,
            "aud": MFA_AUDIENCE,
            "iat": now,
            "exp": now + timedelta(seconds=settings.WEBAUTHN_CHALLENGE_TTL_SECONDS),
            "challenge_id": str(challenge_id),
        },
        settings.AUTH_SECRET_KEY,
        algorithm="HS256",
    )


def decode_mfa_ticket(ticket: str) -> UUID:
    try:
        payload = jwt.decode(
            ticket,
            settings.AUTH_SECRET_KEY,
            algorithms=["HS256"],
            audience=MFA_AUDIENCE,
            issuer=settings.AUTH_ISSUER,
        )
        challenge_id = payload.get("challenge_id")
        if not isinstance(challenge_id, str):
            raise ValueError("Missing challenge")
        return UUID(challenge_id)
    except (jwt.PyJWTError, ValueError) as exc:
        raise AppError(
            "invalid_webauthn_challenge",
            "This security verification has expired. Please try again.",
            status_code=400,
        ) from exc


async def exchange_code(code: str, state: dict[str, str]) -> GoogleClaims:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            token_response = await client.post(
                GOOGLE_TOKEN_ENDPOINT,
                data={
                    "code": code,
                    "client_id": settings.AUTH_GOOGLE_CLIENT_ID,
                    "client_secret": settings.AUTH_GOOGLE_CLIENT_SECRET,
                    "redirect_uri": settings.AUTH_GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code",
                    "code_verifier": state["verifier"],
                },
            )
            token_response.raise_for_status()
            token_payload = token_response.json()
            if not isinstance(token_payload, dict):
                raise ValueError("Invalid token response")
            id_token = token_payload.get("id_token")
            if not isinstance(id_token, str):
                raise ValueError("Missing ID token")
            header = jwt.get_unverified_header(id_token)
            kid = header.get("kid")
            if not isinstance(kid, str):
                raise ValueError("Missing ID token key identifier")
            jwks_response = await client.get(GOOGLE_JWKS_ENDPOINT)
            jwks_response.raise_for_status()
            jwks_payload = jwks_response.json()
            if not isinstance(jwks_payload, dict):
                raise ValueError("Invalid key response")
            keys = jwks_payload.get("keys", [])
            if not isinstance(keys, list):
                raise ValueError("Invalid key set")
            jwk = next(
                (item for item in keys if isinstance(item, dict) and item.get("kid") == kid),
                None,
            )
            if not isinstance(jwk, dict):
                raise ValueError("Unknown ID token key")
            signing_key = jwt.PyJWK.from_dict(jwk).key
            claims = jwt.decode(
                id_token,
                signing_key,
                algorithms=["RS256"],
                audience=settings.AUTH_GOOGLE_CLIENT_ID,
                options={"verify_iss": False},
            )
    except (httpx.HTTPError, jwt.PyJWTError, ValueError, KeyError, TypeError) as exc:
        raise AppError(
            "google_oauth_failed",
            "Google sign-in could not be completed. Please try again.",
            status_code=401,
        ) from exc

    issuer = claims.get("iss")
    subject = claims.get("sub")
    email = claims.get("email")
    verified = claims.get("email_verified")
    nonce = claims.get("nonce")
    authorized_party = claims.get("azp")
    if (
        issuer not in GOOGLE_ISSUERS
        or not isinstance(subject, str)
        or not isinstance(email, str)
        or verified is not True
        or not isinstance(nonce, str)
        or not hmac.compare_digest(nonce, state["nonce"])
        or (authorized_party is not None and authorized_party != settings.AUTH_GOOGLE_CLIENT_ID)
    ):
        raise AppError(
            "google_identity_unverified",
            "Google did not provide a verified identity.",
            status_code=401,
        )
    name = claims.get("name")
    display_name = name.strip() if isinstance(name, str) and name.strip() else email.split("@", 1)[0]
    return GoogleClaims(subject=subject, email=normalize_email(email), display_name=display_name[:120])


def resolve_identity(
    db: Session, claims: GoogleClaims, locale: str
) -> tuple[User, Organization, Workspace]:
    identity = db.scalar(
        select(ExternalIdentity).where(
            ExternalIdentity.provider == "google",
            ExternalIdentity.provider_subject == claims.subject,
        )
    )
    try:
        if identity is not None:
            user = db.get(User, identity.user_id)
            if user is None or not user.is_active:
                raise AppError(
                    "account_unavailable", "This account is not available.", status_code=403
                )
            organization, workspace = load_account_context(db, user)
        else:
            user = db.scalar(select(User).where(User.email == claims.email))
            if user is None:
                user, organization, workspace = create_personal_account(
                    db,
                    email=claims.email,
                    display_name=claims.display_name,
                    locale=locale,
                    password_hash=None,
                )
            else:
                if not user.is_active:
                    raise AppError(
                        "account_unavailable", "This account is not available.", status_code=403
                    )
                organization, workspace = load_account_context(db, user)
            db.add(
                ExternalIdentity(
                    user_id=user.id,
                    provider="google",
                    provider_subject=claims.subject,
                    email_at_link=claims.email,
                )
            )
            db.flush()
        db.commit()
        return user, organization, workspace
    except IntegrityError as exc:
        db.rollback()
        raise AppError(
            "google_account_link_failed",
            "Google sign-in could not be linked safely.",
            status_code=409,
        ) from exc

import binascii
import hmac
import json
import secrets
import string
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from webauthn import (
    generate_authentication_options,
    generate_registration_options,
    options_to_json,
    verify_authentication_response,
    verify_registration_response,
)
from webauthn.helpers import base64url_to_bytes
from webauthn.helpers.exceptions import InvalidAuthenticationResponse, InvalidRegistrationResponse
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    AuthenticatorTransport,
    PublicKeyCredentialDescriptor,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

from app.config import get_settings
from app.modules.identity.models import (
    RecoveryCode,
    User,
    WebAuthnChallenge,
    WebAuthnCredential,
)
from app.modules.identity.schemas import (
    AuthResponse,
    WebAuthnCredentialResponse,
    WebAuthnOptionsResponse,
    WebAuthnRegistrationResponse,
    WebAuthnRequiredResponse,
    WebAuthnStatusResponse,
)
from app.modules.identity.service import issue_session, load_account_context, normalized_utc
from app.platform.errors import AppError

settings = get_settings()
RECOVERY_ALPHABET = string.ascii_uppercase + string.digits


def _options_dict(options: object) -> dict[str, Any]:
    parsed = json.loads(options_to_json(options))  # type: ignore[arg-type]
    if not isinstance(parsed, dict):
        raise RuntimeError("WebAuthn options did not serialize to an object")
    return parsed


def _credential_descriptors(
    credentials: list[WebAuthnCredential],
) -> list[PublicKeyCredentialDescriptor]:
    descriptors: list[PublicKeyCredentialDescriptor] = []
    for credential in credentials:
        transports = [
            AuthenticatorTransport(value)
            for value in credential.transports.split(",")
            if value in {item.value for item in AuthenticatorTransport}
        ]
        descriptors.append(
            PublicKeyCredentialDescriptor(
                id=credential.credential_id,
                transports=transports or None,
            )
        )
    return descriptors


def _store_challenge(
    db: Session, user_id: UUID, purpose: str, challenge: bytes
) -> WebAuthnChallenge:
    record = WebAuthnChallenge(
        user_id=user_id,
        purpose=purpose,
        challenge=challenge,
        expires_at=datetime.now(UTC)
        + timedelta(seconds=settings.WEBAUTHN_CHALLENGE_TTL_SECONDS),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def _consume_challenge(
    db: Session, challenge_id: UUID, purpose: str, user_id: UUID | None = None
) -> WebAuthnChallenge:
    record = db.scalar(
        select(WebAuthnChallenge)
        .where(WebAuthnChallenge.id == challenge_id)
        .with_for_update()
    )
    now = datetime.now(UTC)
    if (
        record is None
        or record.purpose != purpose
        or record.consumed_at is not None
        or normalized_utc(record.expires_at) <= now
        or (user_id is not None and record.user_id != user_id)
    ):
        raise AppError(
            "invalid_webauthn_challenge",
            "This security verification has expired. Please try again.",
            status_code=400,
        )
    # Consume before verification. A failed response cannot be replayed.
    record.consumed_at = now
    db.commit()
    return record


def registration_options(db: Session, user: User) -> WebAuthnOptionsResponse:
    credentials = list(
        db.scalars(select(WebAuthnCredential).where(WebAuthnCredential.user_id == user.id))
    )
    options = generate_registration_options(
        rp_id=settings.WEBAUTHN_RP_ID,
        rp_name=settings.WEBAUTHN_RP_NAME,
        user_id=user.id.bytes,
        user_name=user.email,
        user_display_name=user.display_name,
        exclude_credentials=_credential_descriptors(credentials),
        authenticator_selection=AuthenticatorSelectionCriteria(
            resident_key=ResidentKeyRequirement.PREFERRED,
            user_verification=UserVerificationRequirement.REQUIRED,
        ),
    )
    challenge = _store_challenge(db, user.id, "registration", options.challenge)
    return WebAuthnOptionsResponse(challenge_id=challenge.id, options=_options_dict(options))


def _recovery_hash(code: str) -> str:
    normalized = code.replace("-", "").strip().upper().encode("utf-8")
    return hmac.digest(settings.AUTH_SECRET_KEY.encode("utf-8"), normalized, "sha256").hex()


def _create_recovery_codes(db: Session, user_id: UUID) -> list[str]:
    db.execute(delete(RecoveryCode).where(RecoveryCode.user_id == user_id))
    codes: list[str] = []
    for _ in range(10):
        raw = "".join(secrets.choice(RECOVERY_ALPHABET) for _ in range(12))
        display = f"{raw[:4]}-{raw[4:8]}-{raw[8:]}"
        codes.append(display)
        db.add(RecoveryCode(user_id=user_id, code_hash=_recovery_hash(display)))
    return codes


def verify_registration(
    db: Session,
    user: User,
    challenge_id: UUID,
    credential_payload: dict[str, Any],
) -> WebAuthnRegistrationResponse:
    challenge = _consume_challenge(db, challenge_id, "registration", user.id)
    try:
        verified = verify_registration_response(
            credential=credential_payload,
            expected_challenge=challenge.challenge,
            expected_rp_id=settings.WEBAUTHN_RP_ID,
            expected_origin=settings.WEBAUTHN_ORIGIN,
            require_user_verification=True,
        )
        response_payload = credential_payload.get("response")
        raw_transports = (
            response_payload.get("transports", [])
            if isinstance(response_payload, dict)
            else []
        )
        if not isinstance(raw_transports, list):
            raw_transports = []
        transports = ",".join(
            value
            for value in raw_transports
            if isinstance(value, str) and value in {item.value for item in AuthenticatorTransport}
        )
        credential = WebAuthnCredential(
            user_id=user.id,
            credential_id=verified.credential_id,
            public_key=verified.credential_public_key,
            sign_count=verified.sign_count,
            transports=transports,
            device_type=verified.credential_device_type.value,
            backed_up=verified.credential_backed_up,
            name="Passkey",
        )
        db.add(credential)
        db.flush()
        recovery_codes = _create_recovery_codes(db, user.id) if not user.mfa_enabled else []
        user.mfa_enabled = True
        db.commit()
        return WebAuthnRegistrationResponse(
            credential_id=credential.id,
            credential_name=credential.name,
            recovery_codes=recovery_codes,
        )
    except (InvalidRegistrationResponse, IntegrityError, KeyError, TypeError, ValueError) as exc:
        db.rollback()
        raise AppError(
            "webauthn_registration_failed",
            "The passkey could not be verified. Please try again.",
            status_code=400,
        ) from exc


def authentication_options(db: Session, user: User) -> WebAuthnRequiredResponse:
    credentials = list(
        db.scalars(select(WebAuthnCredential).where(WebAuthnCredential.user_id == user.id))
    )
    if not credentials:
        raise AppError(
            "mfa_unavailable",
            "Account security verification is unavailable. Use a recovery code.",
            status_code=409,
        )
    options = generate_authentication_options(
        rp_id=settings.WEBAUTHN_RP_ID,
        allow_credentials=_credential_descriptors(credentials),
        user_verification=UserVerificationRequirement.REQUIRED,
    )
    challenge = _store_challenge(db, user.id, "authentication", options.challenge)
    return WebAuthnRequiredResponse(challenge_id=challenge.id, options=_options_dict(options))


def pending_authentication_options(
    db: Session, challenge_id: UUID
) -> WebAuthnRequiredResponse:
    challenge = db.get(WebAuthnChallenge, challenge_id)
    if (
        challenge is None
        or challenge.purpose != "authentication"
        or challenge.consumed_at is not None
        or normalized_utc(challenge.expires_at) <= datetime.now(UTC)
    ):
        raise AppError(
            "invalid_webauthn_challenge",
            "This security verification has expired. Please try again.",
            status_code=400,
        )
    credentials = list(
        db.scalars(
            select(WebAuthnCredential).where(WebAuthnCredential.user_id == challenge.user_id)
        )
    )
    options = generate_authentication_options(
        rp_id=settings.WEBAUTHN_RP_ID,
        challenge=challenge.challenge,
        allow_credentials=_credential_descriptors(credentials),
        user_verification=UserVerificationRequirement.REQUIRED,
    )
    return WebAuthnRequiredResponse(challenge_id=challenge.id, options=_options_dict(options))


def verify_authentication(
    db: Session,
    challenge_id: UUID,
    credential_payload: dict[str, Any],
) -> tuple[AuthResponse, str]:
    challenge = _consume_challenge(db, challenge_id, "authentication")
    credential_id = credential_payload.get("id")
    if not isinstance(credential_id, str):
        db.rollback()
        raise AppError(
            "webauthn_authentication_failed", "Security verification failed.", status_code=401
        )
    try:
        decoded_credential_id = base64url_to_bytes(credential_id)
    except (binascii.Error, ValueError) as exc:
        raise AppError(
            "webauthn_authentication_failed", "Security verification failed.", status_code=401
        ) from exc
    credential = db.scalar(
        select(WebAuthnCredential).where(
            WebAuthnCredential.user_id == challenge.user_id,
            WebAuthnCredential.credential_id == decoded_credential_id,
        )
    )
    if credential is None:
        db.rollback()
        raise AppError(
            "webauthn_authentication_failed", "Security verification failed.", status_code=401
        )
    try:
        verified = verify_authentication_response(
            credential=credential_payload,
            expected_challenge=challenge.challenge,
            expected_rp_id=settings.WEBAUTHN_RP_ID,
            expected_origin=settings.WEBAUTHN_ORIGIN,
            credential_public_key=credential.public_key,
            credential_current_sign_count=credential.sign_count,
            require_user_verification=True,
        )
    except (InvalidAuthenticationResponse, KeyError, TypeError, ValueError) as exc:
        db.rollback()
        raise AppError(
            "webauthn_authentication_failed", "Security verification failed.", status_code=401
        ) from exc

    user = db.get(User, challenge.user_id)
    if user is None or not user.is_active or not user.mfa_enabled:
        db.rollback()
        raise AppError(
            "webauthn_authentication_failed", "Security verification failed.", status_code=401
        )
    credential.sign_count = verified.new_sign_count
    credential.device_type = verified.credential_device_type.value
    credential.backed_up = verified.credential_backed_up
    credential.last_used_at = datetime.now(UTC)
    organization, workspace = load_account_context(db, user)
    return issue_session(db, user, organization, workspace)


def verify_recovery_code(
    db: Session, challenge_id: UUID, raw_code: str
) -> tuple[AuthResponse, str]:
    challenge = _consume_challenge(db, challenge_id, "authentication")
    code = db.scalar(
        select(RecoveryCode)
        .where(
            RecoveryCode.user_id == challenge.user_id,
            RecoveryCode.code_hash == _recovery_hash(raw_code),
            RecoveryCode.used_at.is_(None),
        )
        .with_for_update()
    )
    user = db.get(User, challenge.user_id)
    if code is None or user is None or not user.is_active or not user.mfa_enabled:
        db.rollback()
        raise AppError(
            "invalid_recovery_code", "The recovery code is invalid or used.", status_code=401
        )
    code.used_at = datetime.now(UTC)
    organization, workspace = load_account_context(db, user)
    return issue_session(db, user, organization, workspace)


def status(db: Session, user: User) -> WebAuthnStatusResponse:
    credentials = list(
        db.scalars(
            select(WebAuthnCredential)
            .where(WebAuthnCredential.user_id == user.id)
            .order_by(WebAuthnCredential.created_at)
        )
    )
    return WebAuthnStatusResponse(
        enabled=user.mfa_enabled,
        credentials=[
            WebAuthnCredentialResponse(
                id=item.id,
                name=item.name,
                created_at=item.created_at.isoformat(),
                last_used_at=item.last_used_at.isoformat() if item.last_used_at else None,
            )
            for item in credentials
        ],
    )

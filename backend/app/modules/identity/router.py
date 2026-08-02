from urllib.parse import urlencode

from fastapi import APIRouter, Cookie, Depends, Query, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.modules.identity.dependencies import CurrentPrincipal, get_current_principal
from app.modules.identity.google_oauth import (
    create_authorization,
    create_mfa_ticket,
    decode_mfa_ticket,
    decode_state,
    exchange_code,
    resolve_identity,
    safe_return_to,
)
from app.modules.identity.schemas import (
    AuthResponse,
    LocaleUpdateRequest,
    LoginRequest,
    MeResponse,
    RecoveryCodeVerifyRequest,
    RegisterRequest,
    UserResponse,
    WebAuthnOptionsResponse,
    WebAuthnRegistrationResponse,
    WebAuthnRequiredResponse,
    WebAuthnStatusResponse,
    WebAuthnVerifyRequest,
)
from app.modules.identity.service import (
    authenticate_local_user,
    get_me,
    issue_session,
    load_account_context,
    logout,
    refresh,
    register,
    update_locale,
)
from app.modules.identity.webauthn_service import (
    authentication_options,
    pending_authentication_options,
    registration_options,
    status,
    verify_authentication,
    verify_recovery_code,
    verify_registration,
)
from app.platform.errors import AppError
from app.platform.rate_limit import check_rate_limit

router = APIRouter(prefix="/auth", tags=["authentication"])
settings = get_settings()


def set_refresh_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="aikya_refresh",
        value=token,
        max_age=settings.AUTH_REFRESH_TOKEN_TTL_SECONDS,
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite="lax",
        path="/api/v1/auth",
    )


def _web_redirect(path: str, **query: str) -> RedirectResponse:
    suffix = f"?{urlencode(query)}" if query else ""
    return RedirectResponse(f"{settings.AIKYA_PUBLIC_URL.rstrip('/')}{path}{suffix}", status_code=303)


@router.post("/register", response_model=AuthResponse, status_code=201)
def register_user(
    payload: RegisterRequest,
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
) -> AuthResponse:
    identity = f"{request.client.host if request.client else 'unknown'}:{payload.email.lower()}"
    check_rate_limit(
        "register",
        identity,
        limit=settings.AUTH_REGISTER_LIMIT,
        window_seconds=settings.AUTH_RATE_WINDOW_SECONDS,
    )
    auth, refresh_token = register(
        db, payload.email, payload.password, payload.display_name, payload.locale
    )
    set_refresh_cookie(response, refresh_token)
    return auth


@router.post("/login", response_model=AuthResponse | WebAuthnRequiredResponse)
def login_user(
    payload: LoginRequest,
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
) -> AuthResponse | WebAuthnRequiredResponse:
    identity = f"{request.client.host if request.client else 'unknown'}:{payload.email.lower()}"
    check_rate_limit(
        "login",
        identity,
        limit=settings.AUTH_LOGIN_LIMIT,
        window_seconds=settings.AUTH_RATE_WINDOW_SECONDS,
    )
    user = authenticate_local_user(db, payload.email, payload.password)
    if user.mfa_enabled:
        return authentication_options(db, user)
    organization, workspace = load_account_context(db, user)
    auth, refresh_token = issue_session(db, user, organization, workspace)
    set_refresh_cookie(response, refresh_token)
    return auth


@router.get("/oauth/google/start", include_in_schema=False)
def google_start(
    return_to: str | None = Query(default=None),
    locale: str | None = Query(default=None),
) -> RedirectResponse:
    try:
        authorization = create_authorization(return_to, locale)
    except AppError:
        return _web_redirect("/login", oauth_error="google_not_configured")
    response = RedirectResponse(authorization.url, status_code=302)
    response.set_cookie(
        "aikya_google_oauth",
        authorization.cookie,
        max_age=settings.AUTH_OAUTH_STATE_TTL_SECONDS,
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite="lax",
        path="/api/v1/auth/oauth/google",
    )
    return response


@router.get("/oauth/google/callback", include_in_schema=False)
async def google_callback(
    code: str | None = Query(default=None),
    state: str | None = Query(default=None),
    error: str | None = Query(default=None),
    aikya_google_oauth: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    if error or not code or not state or not aikya_google_oauth:
        response = _web_redirect("/login", oauth_error="google_cancelled")
    else:
        try:
            oauth_state = decode_state(aikya_google_oauth, state)
            claims = await exchange_code(code, oauth_state)
            user, organization, workspace = resolve_identity(db, claims, oauth_state["locale"])
            if user.mfa_enabled:
                challenge = authentication_options(db, user)
                response = _web_redirect("/login", oauth_mfa="required")
                response.set_cookie(
                    "aikya_google_mfa",
                    create_mfa_ticket(challenge.challenge_id),
                    max_age=settings.WEBAUTHN_CHALLENGE_TTL_SECONDS,
                    httponly=True,
                    secure=settings.AUTH_COOKIE_SECURE,
                    samesite="lax",
                    path="/api/v1/auth/webauthn",
                )
            else:
                _, refresh_token = issue_session(db, user, organization, workspace)
                response = _web_redirect(safe_return_to(oauth_state["return_to"]))
                set_refresh_cookie(response, refresh_token)
        except AppError as exc:
            db.rollback()
            response = _web_redirect("/login", oauth_error=exc.code)
    response.delete_cookie("aikya_google_oauth", path="/api/v1/auth/oauth/google")
    return response


@router.get("/webauthn/status", response_model=WebAuthnStatusResponse)
def webauthn_status(
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> WebAuthnStatusResponse:
    return status(db, principal.user)


@router.get("/webauthn/oauth/options", response_model=WebAuthnRequiredResponse)
def google_webauthn_options(
    aikya_google_mfa: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> WebAuthnRequiredResponse:
    if not aikya_google_mfa:
        raise AppError(
            "invalid_webauthn_challenge",
            "This security verification has expired. Please try again.",
            status_code=400,
        )
    return pending_authentication_options(db, decode_mfa_ticket(aikya_google_mfa))


@router.post("/webauthn/register/options", response_model=WebAuthnOptionsResponse)
def webauthn_registration_options(
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> WebAuthnOptionsResponse:
    return registration_options(db, principal.user)


@router.post("/webauthn/register/verify", response_model=WebAuthnRegistrationResponse)
def webauthn_registration_verify(
    payload: WebAuthnVerifyRequest,
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> WebAuthnRegistrationResponse:
    return verify_registration(db, principal.user, payload.challenge_id, payload.credential)


@router.post("/webauthn/authenticate/verify", response_model=AuthResponse)
def webauthn_authentication_verify(
    payload: WebAuthnVerifyRequest,
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
) -> AuthResponse:
    check_rate_limit(
        "webauthn_verify",
        request.client.host if request.client else "unknown",
        limit=settings.AUTH_LOGIN_LIMIT,
        window_seconds=settings.AUTH_RATE_WINDOW_SECONDS,
    )
    auth, refresh_token = verify_authentication(db, payload.challenge_id, payload.credential)
    set_refresh_cookie(response, refresh_token)
    response.delete_cookie("aikya_google_mfa", path="/api/v1/auth/webauthn")
    return auth


@router.post("/webauthn/recovery/verify", response_model=AuthResponse)
def webauthn_recovery_verify(
    payload: RecoveryCodeVerifyRequest,
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
) -> AuthResponse:
    check_rate_limit(
        "recovery_verify",
        request.client.host if request.client else "unknown",
        limit=settings.AUTH_LOGIN_LIMIT,
        window_seconds=settings.AUTH_RATE_WINDOW_SECONDS,
    )
    auth, refresh_token = verify_recovery_code(db, payload.challenge_id, payload.recovery_code)
    set_refresh_cookie(response, refresh_token)
    response.delete_cookie("aikya_google_mfa", path="/api/v1/auth/webauthn")
    return auth


@router.post("/refresh", response_model=AuthResponse)
def refresh_session(
    response: Response,
    aikya_refresh: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> AuthResponse:
    if not aikya_refresh:
        raise AppError("invalid_refresh_token", "The session has expired.", status_code=401)
    auth, refresh_token = refresh(db, aikya_refresh)
    set_refresh_cookie(response, refresh_token)
    return auth


@router.post("/logout", status_code=204)
def logout_user(
    response: Response,
    aikya_refresh: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> None:
    logout(db, aikya_refresh)
    response.delete_cookie("aikya_refresh", path="/api/v1/auth")


@router.get("/me", response_model=MeResponse)
def current_user(
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> MeResponse:
    return get_me(db, principal.user, principal.organization_id)


@router.patch("/me/locale", response_model=UserResponse)
def change_locale(
    payload: LocaleUpdateRequest,
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> UserResponse:
    return update_locale(db, principal.user, payload.locale)

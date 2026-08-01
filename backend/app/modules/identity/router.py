from fastapi import APIRouter, Cookie, Depends, Request, Response
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.modules.identity.dependencies import CurrentPrincipal, get_current_principal
from app.modules.identity.schemas import AuthResponse, LoginRequest, MeResponse, RegisterRequest
from app.modules.identity.service import get_me, login, logout, refresh, register
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
    auth, refresh_token = register(db, payload.email, payload.password, payload.display_name)
    set_refresh_cookie(response, refresh_token)
    return auth


@router.post("/login", response_model=AuthResponse)
def login_user(
    payload: LoginRequest,
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
) -> AuthResponse:
    identity = f"{request.client.host if request.client else 'unknown'}:{payload.email.lower()}"
    check_rate_limit(
        "login",
        identity,
        limit=settings.AUTH_LOGIN_LIMIT,
        window_seconds=settings.AUTH_RATE_WINDOW_SECONDS,
    )
    auth, refresh_token = login(db, payload.email, payload.password)
    set_refresh_cookie(response, refresh_token)
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

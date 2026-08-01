from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=None, case_sensitive=True, extra="ignore")

    AIKYA_ENV: str = "development"
    AIKYA_LOG_LEVEL: str = "INFO"
    AIKYA_API_URL: str = "http://localhost:8000"
    DATABASE_URL: str = (
        "postgresql+psycopg://aikya_dev:development-only-change-me@postgres:5432/aikya_dev"
    )
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    STORAGE_ENDPOINT: str = "http://minio:9000"
    STORAGE_PUBLIC_ENDPOINT: str = "http://localhost:9000"
    STORAGE_REGION: str = "us-east-1"
    STORAGE_BUCKET_QUARANTINE: str = "aikya-quarantine"
    STORAGE_BUCKET_DOCUMENTS: str = "aikya-documents"
    STORAGE_BUCKET_OUTPUTS: str = "aikya-outputs"
    STORAGE_ACCESS_KEY: str = "aikya-local-access"
    STORAGE_SECRET_KEY: str = "development-only-storage-secret"
    STORAGE_USE_PATH_STYLE: bool = True
    SIGNED_URL_TTL_SECONDS: int = 300
    SIGNED_DOWNLOAD_TTL_SECONDS: int = 300

    AUTH_SECRET_KEY: str = "development-only-auth-secret-change-before-production-32bytes"
    AUTH_ISSUER: str = "aikya-ai"
    AUTH_AUDIENCE: str = "aikya-web"
    AUTH_ACCESS_TOKEN_TTL_SECONDS: int = 900
    AUTH_REFRESH_TOKEN_TTL_SECONDS: int = 2_592_000
    AUTH_COOKIE_SECURE: bool = False

    ALLOWED_ORIGINS: str = "http://localhost:5173"
    MAX_UPLOAD_BYTES: int = 52_428_800
    MAX_DOCUMENT_PAGES: int = 100
    MAX_TEXT_TRANSLATION_CHARACTERS: int = 10_000
    TEMPORARY_FILE_RETENTION_HOURS: int = 24

    TRANSLATION_DEFAULT_PROVIDER: str = "libretranslate"
    LIBRETRANSLATE_URL: str = ""
    LIBRETRANSLATE_API_KEY: str = ""
    TRANSLATION_REQUEST_TIMEOUT_SECONDS: float = 30.0
    AUTH_LOGIN_LIMIT: int = 10
    AUTH_REGISTER_LIMIT: int = 5
    AUTH_RATE_WINDOW_SECONDS: int = 900
    TRANSLATION_RATE_LIMIT: int = 30
    UPLOAD_RATE_LIMIT: int = 10
    WORKLOAD_RATE_WINDOW_SECONDS: int = 60
    CLAMAV_HOST: str = "clamav"
    CLAMAV_PORT: int = 3310
    CLAMAV_TIMEOUT_SECONDS: float = 30.0
    CLAMAV_CHUNK_BYTES: int = 1_048_576

    @field_validator("AUTH_SECRET_KEY")
    @classmethod
    def validate_auth_secret(cls, value: str, info: object) -> str:
        if len(value.encode("utf-8")) < 32:
            raise ValueError("AUTH_SECRET_KEY must contain at least 32 bytes")
        return value

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    if settings.AIKYA_ENV == "production" and "development-only" in settings.AUTH_SECRET_KEY:
        raise ValueError("Production AUTH_SECRET_KEY must be supplied securely")
    return settings

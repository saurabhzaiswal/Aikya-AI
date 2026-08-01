from dataclasses import dataclass

import httpx

from app.config import get_settings
from app.platform.errors import AppError


@dataclass(frozen=True)
class ProviderTranslation:
    translated_text: str
    detected_language: str | None


class LibreTranslateProvider:
    name = "libretranslate"

    def __init__(self) -> None:
        self.settings = get_settings()

    def translate(
        self, text: str, source_language: str, target_language: str
    ) -> ProviderTranslation:
        if not self.settings.LIBRETRANSLATE_URL:
            raise AppError(
                "translation_provider_unconfigured",
                "Translation is not configured yet. Add a provider in the server environment.",
                status_code=503,
            )
        payload: dict[str, str] = {
            "q": text,
            "source": source_language,
            "target": target_language,
            "format": "text",
        }
        if self.settings.LIBRETRANSLATE_API_KEY:
            payload["api_key"] = self.settings.LIBRETRANSLATE_API_KEY
        try:
            with httpx.Client(timeout=self.settings.TRANSLATION_REQUEST_TIMEOUT_SECONDS) as client:
                response = client.post(
                    f"{self.settings.LIBRETRANSLATE_URL.rstrip('/')}/translate", json=payload
                )
                response.raise_for_status()
                data = response.json()
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            raise AppError(
                "translation_provider_unavailable",
                "The translation provider is temporarily unavailable.",
                status_code=503,
                retryable=True,
            ) from exc
        except httpx.HTTPStatusError as exc:
            retryable = exc.response.status_code >= 500 or exc.response.status_code == 429
            raise AppError(
                "translation_provider_unavailable"
                if retryable
                else "translation_provider_rejected",
                "The translation provider could not process this request.",
                status_code=503 if retryable else 422,
                retryable=retryable,
            ) from exc
        except (ValueError, TypeError, KeyError) as exc:
            raise AppError(
                "translation_provider_invalid_response",
                "The translation provider returned an invalid response.",
                status_code=502,
                retryable=True,
            ) from exc

        translated = data.get("translatedText")
        if not isinstance(translated, str) or not translated:
            raise AppError(
                "translation_provider_invalid_response",
                "The translation provider returned an invalid response.",
                status_code=502,
                retryable=True,
            )
        detected = data.get("detectedLanguage")
        detected_code = detected.get("language") if isinstance(detected, dict) else None
        return ProviderTranslation(translated_text=translated, detected_language=detected_code)


def get_translation_provider() -> LibreTranslateProvider:
    settings = get_settings()
    if settings.TRANSLATION_DEFAULT_PROVIDER != "libretranslate":
        raise AppError(
            "translation_provider_unconfigured",
            "The configured translation provider is not supported by this build.",
            status_code=503,
        )
    return LibreTranslateProvider()

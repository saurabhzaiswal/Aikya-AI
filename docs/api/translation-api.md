# Translation API Contract — Phase 1

Base path: `/api/v1/translation`

## Provider contract

Phase 1 uses an internal provider-neutral interface and a configurable LibreTranslate-compatible HTTP adapter. Provider URLs/keys remain server-side. The adapter normalizes language codes, timeouts, capabilities, response, and safe errors.

## `GET /languages`

Returns supported language codes/names/direction based on the configured provider/capability baseline. It does not reveal secrets.

## `POST /text`

Requires authentication. Accepts source text, target language, and optional source language (`auto` allowed). Enforces configured character limit and rate/usage policy. Returns translation ID, source/target language, translated text, provider-neutral state, and timestamp.

## `GET /history`

Returns the authenticated tenant's recent text translations with bounded pagination. Phase 1 returns content because this is a user history feature; logs/analytics must not copy it.

## Errors

- `translation_provider_unconfigured`
- `translation_pair_unsupported`
- `translation_input_too_large`
- `translation_provider_unavailable` (retryable)
- `translation_provider_rejected`

Raw provider errors, keys, and payloads are never returned or logged.

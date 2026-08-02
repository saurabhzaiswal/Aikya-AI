# Changelog

All notable user/developer-visible changes follow Keep a Changelog-style categories and semantic versioning once releases begin.

## Unreleased

### Added

- Original Aikya convergence/bridge logo system, favicon, web manifest, lightweight route-grouped social artwork, complete Open Graph/X image metadata, and logo-aware public structured data.
- Real Google-only sign-in with Authorization Code + PKCE, verified-email account linking, and rotating HttpOnly sessions.
- WebAuthn passkey two-factor authentication with Windows Hello/device/security-key support and one-time hashed recovery codes.
- Tactile raised/pressed interaction states across shared primary/secondary authentication and product controls, plus the official multicolor Google G mark.
- Responsive login/register experience with placeholders, accessible client validation, password confirmation/checklist, bounded toast feedback, reliable post-authentication redirects, and lifecycle-free ripple interactions across buttons.
- ADR-017 covering the existing rotating HttpOnly refresh session and the security gates for future Google, Microsoft, LinkedIn, Facebook, X, and MFA support.
- Production engineering documentation foundation and editable diagrams.
- Docker development and production reference configuration.
- AI-agent operating system, progress tracking, contribution rules, API planning, and ADR baseline.
- Unified Nuxt 4 Phase 1 application with SSR public pages, SEO metadata, content-backed blog/docs, and a client-rendered Vue Options API workspace for authentication, text translation/history, and digital-PDF translation/download workflows.
- Proprietary license, legal-document drafts, founder attribution, and verified public profile links.
- FastAPI modular backend with personal tenant bootstrap, Argon2id passwords, short-lived JWT access tokens, rotating hashed refresh sessions, rate limiting, and tenant-scoped resources.
- LibreTranslate-compatible translation adapter, signed private S3 upload/download flow, durable Celery document jobs, PyMuPDF extraction/readable export, and fail-closed ClamAV scanning.
- SQLAlchemy models, initial Alembic migration, dependency lockfiles, real development containers, one-shot storage/migration setup, health endpoints, and production reference images.
- Node.js 24.18.x and Python 3.14 runtime baselines, native UUIDv7 persisted identifiers, Nuxt i18n English/Hindi catalogs with English fallback, a locale switcher, frontend memory-safety policy, root operator runbook, and GitHub Actions CI for `master`.

### Security

- Google state, nonce, PKCE, issuer/audience/signature/expiry validation and safe internal redirects; enabled Aikya MFA cannot be bypassed through Google login.
- One-time WebAuthn challenges, verified-user assertions, authenticator signature counters, and keyed-hash recovery-code storage.
- Synchronized the local-registration password boundary at 8–128 characters with a three-of-four character-class requirement across Nuxt and FastAPI.
- Added content-safe API errors, short-lived signed URLs, checksum/signature/size/page validation, private buckets, randomized object keys, and scanner-gated quarantine promotion.
- Added retry-safe session-family revocation and document processing recovery behavior.

### Known limitations

- Full Docker runtime acceptance, real translation-provider integration, live Google callback acceptance with founder-owned credentials, visual browser QA, active deletion/retention automation, automated suites, credential reset/revocation UX, authentication audit events, and final security review remain open before private beta.

## 0.1.0 - 2026-08-01

### Added

- Initial Aikya AI repository foundation.

# Changelog

All notable user/developer-visible changes follow Keep a Changelog-style categories and semantic versioning once releases begin.

## Unreleased

### Added

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

- Added content-safe API errors, short-lived signed URLs, checksum/signature/size/page validation, private buckets, randomized object keys, and scanner-gated quarantine promotion.
- Added retry-safe session-family revocation and document processing recovery behavior.

### Known limitations

- Nuxt lint/type/build acceptance, full Docker runtime acceptance, real provider integration, visual browser QA, active deletion/retention automation, automated suites, and final security review remain open before private beta.

## 0.1.0 — 2026-08-01

### Added

- Initial Aikya AI repository foundation.

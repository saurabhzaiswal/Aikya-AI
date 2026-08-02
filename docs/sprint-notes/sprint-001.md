# Sprint 001 - Foundation to Phase 1 MVP

Date started: 2026-08-01  
Owner: Saurabh Choudhary with AI engineering assistance  
Status: Nuxt migration implemented; frontend and runtime acceptance pending

## Goal

Complete repository governance and deliver only the Phase 1 MVP: authentication, dashboard, text translation, PDF upload/basic translation, and export.

## Scope

- AI-agent operating system and progress discipline.
- Nuxt 4 frontend foundation with Vue 3 Options API feature components.
- FastAPI modular backend foundation.
- Personal tenant authentication.
- Provider-neutral text translation.
- Basic digital PDF workflow.
- Docker integration and documentation synchronization.

## Explicitly excluded

OCR, AI enhancement, audio, resume workflow, extension, mobile, desktop, billing, teams, public API, and enterprise controls.

## Risks

- External registry connectivity can delay dependency-image pulls; retry transient TLS failures without weakening transport security.
- Real translation requires configured provider access.
- PDF reconstruction quality is bounded and must be represented honestly.
- Automated suites are deferred; verification evidence must not be overstated.

## Completion notes

Completed on 2026-08-01:

- Established root/public agent guidance, ignored private context, governance, status/progress discipline, ADRs, and the complete documentation foundation.
- Migrated the application to Nuxt 4 with SSR public pages, SEO and content routes, registration/login, personal dashboard, text translation/history, digital-PDF upload/progress/download, dark mode, responsive behavior, and explicit limitations.
- Implemented the FastAPI modular backend, SQLAlchemy/Alembic data layer, rotating refresh sessions, tenant-scoped access, Redis rate limits, LibreTranslate-compatible adapter, signed S3 storage, Celery jobs, PyMuPDF extraction/readable export, and fail-closed ClamAV scan.
- Replaced placeholder topology with development builds and a production reference for frontend, API, worker, migration, PostgreSQL, Redis, MinIO bucket initialization, and ClamAV.
- Added the Node 24.18.x/Python 3.14 runtime contract, shared UUIDv7 persisted IDs, Nuxt i18n English/Hindi foundation, frontend memory-safety policy, operator runbook, and GitHub CI without CD.
- Expanded localization to a browser-first 23-locale Global/Indian/Bihar registry with visible grouping, one-time feedback, cookie/account persistence, privacy rules, and safe catalog fallbacks.
- Optimized Docker build contexts and production stages, documented measured cache/artifact causes, and added Buildx cache reuse for CI without changing business logic.
- Fixed locale-aware post-authentication navigation, implemented Google-only Authorization Code + PKCE and WebAuthn passkey 2FA with recovery codes, migrated native PostgreSQL to `20260802_0002`, and added shared tactile press feedback for primary authentication/product controls.

Verification evidence:

- Nuxt lint and typecheck pass. Client/SSR compilation, 31-route prerendering, generated Nitro HTTP/SEO smoke, and the optimized production container build pass.
- Backend Ruff, strict mypy (35 source files), compile, OpenAPI generation (18 paths), and Alembic upgrade passed.
- The authentication extension passes backend Ruff and strict mypy across 38 source files, import/OpenAPI and OAuth state/nonce/PKCE smokes, Nuxt ESLint/typecheck, and Alembic upgrade to `20260802_0002`.
- Synthetic authentication/session rotation, text-provider/history, upload validation, PDF render/full job, and clamd clean/infected/unavailable flows passed.
- Compose YAML structure, required files, relative Markdown links, ignored private files, Vue Options API usage, component color tokens, and common credential patterns passed static checks.

Outstanding acceptance:

- Frontend/backend production image builds and isolated container smokes pass. The pinned ClamAV image succeeded on retry; core Compose services reached healthy/start-complete states, but final ClamAV/worker acceptance was interrupted by a local Docker Desktop container-inspect HTTP 500 and daemon unresponsiveness.
- Real provider/MinIO/Redis/Celery/ClamAV integration and browser visual QA remain unverified here.
- Active deletion/retention automation, automated security/tenant coverage, restore/security drills, and final security review are required before private beta.
- Automated test suites were intentionally not added under the founder's current instruction.

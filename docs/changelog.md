# Engineering Documentation Changelog

## 2026-08-01

- Created the production product, architecture, data, API, UX, security, deployment, testing, business, pricing, and brand foundation.
- Added six editable Excalidraw diagrams.
- Added Docker development and reference production configuration.
- Added private AI-agent operating context and public AGENTS entry point.
- Added founder/ownership context, strict project status/progress tracking, API/feature documentation areas, ADRs, observability, backup/recovery, and future-scope boundary.
- Implemented and documented the Phase 1 Vue/FastAPI/Celery vertical slice for authentication, dashboard, text translation, and basic digital-PDF translation/export.
- Added the initial migration, provider/storage interfaces, rate limits, secure rotating sessions, signed object flow, malware scanner, and real development/production Compose roles.
- Recorded passed static/build/migration/synthetic-smoke evidence and the outstanding Docker, provider, visual-QA, deletion, automated-test, and security-review gates.
- Accepted ADR-014 and migrated the unified web frontend from Vite SPA delivery to Nuxt 4 SSR/Nitro, including public SEO pages, content collections, typed services, proprietary licensing, legal drafts, and founder attribution.
- Recorded passing Nuxt lint/typecheck, client and SSR compilation, 31-route prerendering, and generated Nitro HTTP/SEO smoke checks. Final dependency tracing/container packaging remains open because the local Windows build exceeded its timeout.
- Validated all Compose YAML and frontend manifest syntax, repository-relative Markdown links, Options API component enforcement, service-only API access, and a zero-vulnerability production dependency audit.
- Accepted ADR-015 and added Python 3.14/native UUIDv7 persistence, Node 24.18.x, official Nuxt i18n English fallback/Hindi routing, frontend lifecycle memory-safety rules, a canonical runbook, and CI-only GitHub Actions validation for `master`.
- Accepted ADR-016 and added the 23-locale Global/Indian/Bihar registry, browser-first one-time detection, grouped language switcher, Preview/fallback policy, and authenticated locale persistence without IP geolocation.
- Corrected the CI-reported locale template type boundary by preserving registry literal types and validating selector input; applied the non-localhost site URL to all frontend CI steps.

This file records engineering-foundation history. User/developer-visible release changes belong in the root `CHANGELOG.md`.

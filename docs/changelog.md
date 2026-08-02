# Engineering Documentation Changelog

## 2026-08-02

- Fixed the authenticated locale/navigation race that sent successful login and registration back to the landing page; dashboard routes are locale-aware and account-locale application is awaited.
- Added real Google-only OpenID Connect Authorization Code + PKCE, verified-email account linking, signed state/nonce, safe redirects, and the existing rotating HttpOnly refresh session.
- Added WebAuthn passkey 2FA enrollment and enforcement after password or Google authentication, UUIDv7 credential/challenge records, signature counters, and one-time recovery codes stored only as keyed hashes.
- Added `webauthn`, `PyJWT[crypto]`, and `@simplewebauthn/browser` for standards-based server verification, signed Google identity validation, and browser WebAuthn ceremonies respectively.
- Replaced the temporary Google letter treatment with the official fixed-color multicolor G SVG and introduced shared raised/pressed primary, secondary, and Google button states with focus and reduced-motion coverage.
- Redesigned login and registration with responsive auth layout, placeholders, password visibility, accessible field validation, an 8–128 character password contract, password confirmation/checklist, bounded toast feedback, reliable component-router redirects after async authentication, and project-wide lifecycle-free CSS ripple coverage.
- Recorded ADR-017: retain rotating HttpOnly refresh sessions, require operational provider flows before showing Google/Microsoft/LinkedIn/Facebook/X sign-in, and defer MFA until enrollment/recovery/audit controls exist.
- Kept login and registration directly reachable by removing guest-page auto-redirects, enabled locale-aware auth routes, and restored localized `NuxtLink` targets so non-English navigation cannot fall back to the landing page.
- Standardized native Nuxt on port 3000 with FastAPI on 8000 across package scripts, environment contracts, lifecycle scripts, CORS/site URLs, Compose host mapping, and local documentation.
- Replaced localized public navigation route objects with relative `$localePath(...)` strings and used literal relative anchors for non-localized `/login` and `/register` routes. This prevents empty auth hrefs and absolute-current-page payload prefetch; the preview “Translate text” control is now a real registration link.
- Corrected the native Nitro proxy mount so same-origin `/api/v1/**` requests retain the backend `/api` prefix when forwarded to FastAPI on port 8000.
- Added a theme-aware brand-token scrollbar for Firefox and WebKit browsers without introducing component-local colors.
- Added pointer, hover, pressed, and reduced-motion-aware CSS ripple states to shared primary/secondary actions.
- Separated native and Docker database configuration: FastAPI/Alembic now load the absolute ignored root `.env.local`, process/Compose values retain priority, and committed examples use `localhost` natively versus `postgres` inside Compose.
- Added a password-masked database configuration/connection diagnostic and documented Windows CMD, PowerShell, Git Bash, pgAdmin, database creation, and Alembic workflows.
- Removed the backend-refresh wait from guest-route navigation so login/register forms render immediately even while the API or database is unavailable; submission still fails safely until backend readiness passes.
- Corrected Nuxt component discovery so unprefixed Phase 1 component names resolve consistently across SSR and client navigation, restoring the registration route and removing unresolved-component hydration mismatches.
- Allowed both stateful and functional Vue icon components in the feature-card contract, eliminating the Lucide runtime prop warning.
- Added pgAdmin/PostgreSQL credential synchronization guidance and backend virtual-environment lock detection to the native Windows workflow.
- Repaired the native Nuxt installation workflow after an interrupted dependency install left Shiki without a generated Rolldown runtime module.
- Replaced the directly deprecated `lucide-vue-next` dependency with `@lucide/vue`, preserving the existing icon component API and UI behavior.
- Added a Windows frontend-module lock preflight to `setup-local.ps1` and documented safe recovery for Shiki corruption, `EPERM` native-module locks, and upstream-only deprecation notices.
- Marked loopback site URLs as development in Nuxt Site Config while preserving non-loopback production behavior, removing the misleading localhost SEO warning from native prepare/type/build commands.
- Prevented `start-local.ps1` from starting a second Nuxt instance when an Aikya frontend process already owns the generated directories on another port.

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
- Recorded passing Nuxt lint/typecheck, client and SSR compilation, 31-route prerendering, generated Nitro HTTP/SEO smoke checks, and optimized production container packaging.
- Validated all Compose YAML and frontend manifest syntax, repository-relative Markdown links, Options API component enforcement, service-only API access, and a zero-vulnerability production dependency audit.
- Accepted ADR-015 and added Python 3.14/native UUIDv7 persistence, Node 24.18.x, official Nuxt i18n English fallback/Hindi routing, frontend lifecycle memory-safety rules, a canonical runbook, and CI-only GitHub Actions validation for `master`.
- Accepted ADR-016 and added the 23-locale Global/Indian/Bihar registry, browser-first one-time detection, grouped language switcher, Preview/fallback policy, and authenticated locale persistence without IP geolocation.
- Corrected the CI-reported locale template type boundary by preserving registry literal types and validating selector input; applied the non-localhost site URL to all frontend CI steps.
- Reduced Docker contexts from local gigabyte-scale directories to measured sub-megabyte manifests with root/frontend/backend ignore policies, cache-mounted multi-stage Dockerfiles, explicit per-application Compose contexts, a shared backend role image, and scoped Buildx CI caches.
- Verified both production image builds, a frontend container health response, and backend production-image import; recorded the remaining transient dependency-registry pull and full-stack acceptance gate.
- Added a dedicated non-published egress network for ClamAV signature updates and translation-provider calls while keeping PostgreSQL, Redis, and MinIO isolated.
- Confirmed the pinned ClamAV pull succeeds after a transient TLS retry and recorded the remaining local Docker Desktop API failure encountered during full-stack health acceptance.

This file records engineering-foundation history. User/developer-visible release changes belong in the root `CHANGELOG.md`.

# Aikya AI Project Progress Tracker

Version: 0.1.0  
Last updated: 2026-08-02

## Purpose

AI agents must read this file before development. Check completed work, current phase, pending work, and the next logical item. Never rebuild completed work or mark an item complete without verification.

## Current phase

- [x] Foundation documentation
- [x] Architecture design
- [ ] Phase 1 MVP development - implementation complete; runtime/security acceptance pending
- [ ] Private beta
- [ ] Production

## Foundation documentation

- [x] Product vision
- [x] Requirements
- [x] Roadmap
- [x] Architecture
- [x] Database design
- [x] API planning
- [x] UI/UX system
- [x] Security architecture
- [x] Deployment plan
- [x] Testing strategy
- [x] Business model
- [x] Pricing strategy
- [x] Brand guidelines
- [x] Founder and ownership context
- [x] Observability plan
- [x] Backup/recovery plan
- [x] Future-scope boundary

## Architecture diagrams

- [x] System architecture
- [x] Document processing flow
- [x] SaaS architecture
- [x] Database ER overview
- [x] Deployment architecture
- [x] User journey
- [x] Editable `.excalidraw` sources structurally validated
- [x] Architecture approved for Phase 1 implementation through founder instruction dated 2026-08-01

## Repository and environment

- [x] Root README
- [x] Documentation index
- [x] AGENTS entry point and ignored private agent context
- [x] CONTRIBUTING, CODEOWNERS placeholder, license status, changelogs
- [x] Environment templates and separation
- [x] Docker development/production configuration
- [x] PostgreSQL, Redis, worker, storage, frontend, and backend service definitions
- [x] Root local/production runbook and GitHub CI for `master`
- [x] Dedicated Docker build contexts, defensive root/application ignore policies, multi-stage cache strategy, and Buildx CI caches
- [ ] Docker runtime verification - application images, pulls, isolated smokes, and core services pass; final ClamAV/worker and critical-flow verification await Docker Desktop recovery

## Phase 1 MVP

### Frontend foundation

- [x] Nuxt 4 + Vue 3 + TypeScript unified web application
- [x] SSR/prerendered public routes and client-only private route boundary
- [x] Vue Options API enforcement for stateful components, with ADR-014 Nuxt exceptions
- [x] Tailwind CSS and SCSS design-token system
- [x] Pinia, typed Axios services, Nuxt Content, SEO metadata, sitemap, and robots rules
- [x] Responsive public site and workspace shell, dark mode, and accessibility baseline
- [x] Browser-first Nuxt i18n foundation with a 23-locale Global/Indian/Bihar registry, grouped switcher, one-time notice, account/cookie persistence, and English fallback
- [x] Frontend memory-safety ownership and profiling policy

### Backend foundation

- [x] FastAPI modular structure
- [x] SQLAlchemy/PostgreSQL and Alembic migration
- [x] Redis/Celery worker integration
- [x] Configuration, error contract, health endpoints, logging hygiene
- [x] S3-compatible storage adapter
- [x] Python 3.14 runtime baseline and shared UUIDv7 persisted-identifier generator

### Authentication and tenancy

- [x] Registration and personal organization/workspace bootstrap
- [x] Login, access token, rotating refresh cookie, logout
- [x] Current-user/session endpoint
- [x] Tenant-scoped authorization
- [x] Google OpenID Connect Authorization Code + PKCE with verified-email linking
- [x] WebAuthn passkey 2FA for password and Google login with hashed one-time recovery codes
- [x] Locale-safe post-auth redirect to the private dashboard

### Text translation

- [x] Provider-neutral translation contract
- [x] Configurable LibreTranslate-compatible provider
- [x] Text translation API and UI
- [x] Translation history and provider-safe errors

### PDF workflow

- [x] Signed upload intent and completion
- [x] PDF signature/size/checksum/page validation
- [x] Fail-closed malware scan before PDF parsing
- [x] Durable document/job records
- [x] Basic embedded-text extraction
- [x] Asynchronous segment translation
- [x] Basic readable translated PDF export
- [x] Dashboard progress/history/download

### Phase completion

- [x] Nuxt lint and typecheck pass - localization type correction verified locally; clean GitHub/Linux rerun pending
- [x] Client/SSR compilation, 31-route prerendering, and generated-server HTTP/SEO smoke pass
- [x] Final Nitro dependency trace/container build completes - optimized frontend and backend production images built successfully with BuildKit
- [x] Backend static/import/migration checks pass
- [ ] Compose runtime and critical-flow smoke check passes
- [ ] Active document deletion and retention cleanup passes
- [ ] Browser visual/accessibility QA passes
- [ ] Security/privacy review completed
- [x] Documentation, status, progress, sprint note, and changelog synchronized
- [x] Dashboard exposes every approved Phase 1 user workflow: text translation, digital-PDF upload/progress/download, recent activity, session controls, localization/theme, and passkey security

## Future phases - do not build now

- [ ] OCR and scanned-PDF reconstruction
- [ ] Resume translation and browser extension
- [ ] AI explanation/summarization/rewrite
- [ ] Text-to-speech/audio
- [ ] Mobile and desktop clients
- [ ] Billing, teams, public API, and enterprise controls

## Current sprint

Sprint: 001  
Goal: Establish the AI-agent operating system and implement only the Phase 1 MVP.

Current highest-priority item: run native Windows full-stack acceptance with MinIO, WSL Redis/ClamAV, PostgreSQL, Celery, and a trusted translation provider; then complete deletion/retention and security review before beta. Preserve Docker as an inactive alternative.

## Completed work log

### 2026-08-02

Completed:

- Fixed the post-login locale race that redirected authenticated users to the landing page; private dashboard routes now participate in Nuxt i18n and account-locale application is awaited before locale-aware navigation.
- Implemented Google-only OAuth with signed HttpOnly state, nonce, PKCE, verified ID-token/email checks, safe account linking, safe internal return paths, and normal rotating refresh sessions.
- Implemented WebAuthn passkey 2FA enrollment and password/Google login enforcement with one-time challenges, signature counters, UUIDv7 persistence, and ten one-time recovery codes stored only as keyed hashes.
- Added the official multicolor Google SVG mark and shared raised, physically pressed button feedback inspired by tactile language-learning UI patterns without adding lifecycle listeners.
- Redesigned authentication UI, added accessible field validation/placeholders/password confirmation, synchronized the founder-approved 8-character minimum with the API, added bounded toast feedback, and standardized CSS-only ripple coverage without lifecycle listeners.
- Accepted ADR-017 for the existing rotating HttpOnly refresh session and gated future Google/Microsoft/LinkedIn/Facebook/X and MFA work behind real provider/recovery/security implementation.
- Made localized login/register routes directly reachable, removed guest-page auto-redirects, and verified English and Hindi auth routes return HTTP 200.
- Standardized native Nuxt on port 3000 while preserving FastAPI on port 8000 and Docker's internal frontend port.
- Kept localized public navigation relative, corrected non-localized auth routes to literal relative anchors, made the preview “Translate text” CTA interactive, corrected the Nitro `/api` proxy target, and added shared pointer/ripple states plus the brand scrollbar.
- Separated native `.env.local` and Docker `.env` database targets while preserving process-environment precedence for Compose/production.
- Added a password-masked database diagnostic and prevented backend unavailability from blocking login/register form rendering.
- Restored Nuxt registration-route rendering by aligning component auto-registration with the repository's unprefixed component API.
- Added pgAdmin-focused database connection guidance and safe backend `.venv` lock detection for native Windows setup.
- Repaired the interrupted native frontend installation that left Shiki without its generated Rolldown runtime module.
- Migrated all icon imports from deprecated `lucide-vue-next` to `@lucide/vue` and synchronized the npm lockfile.
- Added Windows Node-module lock detection to the native setup/start scripts and documented the exact safe recovery workflow.

Changed:

- Loopback Nuxt site URLs now declare the development environment, removing the misleading localhost SEO warning without weakening production URL validation.
- Native Windows development is the active local workflow; the existing Docker setup remains unchanged and available as an inactive alternative.

Notes:

- Local PostgreSQL successfully upgraded from `20260801_0001` to `20260802_0002`; Google OAuth state/nonce/PKCE safe-return smoke, backend Ruff, strict mypy, import/OpenAPI, Nuxt ESLint, and Nuxt typecheck pass.
- The active dashboard contains the complete founder-approved Phase 1 surface. OCR/scanned-PDF reconstruction, DOCX, AI, billing, teams, extension, mobile, and desktop remain explicitly outside this phase.
- Auth redesign acceptance passes frontend ESLint, generated Nuxt `vue-tsc`, production Nuxt build, zero-vulnerability production audit, backend Ruff/mypy, 8-character password-boundary smoke, button-ripple coverage, and generated-server English/Hindi login/register HTTP smokes. Visual browser review remains pending because no browser-control session was available.
- Frontend ESLint, existing generated Nuxt `vue-tsc`, start-script PowerShell syntax, rendered CTA href inspection, zero absolute-local anchors, 3000/8000 environment consistency, all public/auth HTTP routes, `/signup` redirect, and same-origin proxy 401 behavior pass. Restart once before browser recheck to clear stale payload/HMR state.
- Effective native configuration resolves `localhost:5432/aikya-ai`; effective Compose backend/worker/migrate configuration resolves `postgres:5432/aikya-ai`. The native database exists and is upgraded to migration `20260802_0002`.
- `/login` and `/register` return HTTP 200 promptly in the running native Nuxt server; generated component declarations contain every component used by templates. Form submission remains unavailable until the confirmed missing database is explicitly created and migrated.
- Nuxt prepare, ESLint with zero warnings, Nuxt typecheck, the running dev `/healthz` response, PowerShell syntax, lock-preflight behavior, and npm audit pass; npm reports zero known vulnerabilities.
- A fresh production build was not run concurrently with the founder's healthy manual Nuxt dev process because both commands own `.nuxt`/`.output`. Stop that dev process before the next build verification.
- The remaining `vue-i18n@10` and `glob@10` install notices are upstream transitive dependency notices. Unsafe forced overrides were intentionally not added.

### 2026-08-01

Completed:

- Production foundation documentation and six editable Excalidraw diagrams.
- Docker development and production reference configuration.
- AI-agent operating system, project status/progress tracking, governance, API planning, and ADR baseline.
- Unified Nuxt 4 application with SSR public pages, SEO/content routes, and an Options API dashboard for authentication, text translation, and the PDF workflow.
- FastAPI modular backend with personal tenancy, rotating sessions, rate limits, provider adapter, signed storage, durable jobs, PDF extraction/rendering, and malware scan.
- Real development/production container definitions, lockfiles, initial migration, and static/build/synthetic smoke verification.
- Node.js 24.18.x/Python 3.14 baselines, UUIDv7 ORM identifiers, browser-first 23-locale Nuxt i18n foundation, memory-safety rules, root runbook, and GitHub Actions CI.

Changed:

- Reconciled the web stack to Nuxt 4 with Vue 3 Options API components and a FastAPI modular monolith.
- Limited current implementation to the Phase 1 MVP.
- Replaced ORM UUIDv4 defaults with the shared Python 3.14 UUIDv7 generator while retaining UUIDv4 only for non-persisted request/JWT correlation values.
- Added account/cookie/browser locale priority, Global/Indian/Bihar grouping, Bihar-aware presentation, non-blocking first-visit feedback, and account locale synchronization without IP geolocation.
- Reduced measured Docker context manifests to ~0.811 MB for frontend and ~0.248 MB for backend; retained one shared backend artifact for API/worker/migrate roles.

Notes:

- Docker is available. Optimized production images build successfully; frontend `/healthz` returns HTTP 200 and the backend production image imports successfully.
- Automated test suites are temporarily deferred by explicit founder instruction; build/static/smoke verification remains required.
- Backend Ruff, strict mypy, compile, OpenAPI generation, Alembic upgrade, YAML parsing, link scan, credential-pattern scan, auth/text/PDF synthetic smokes, and clamd protocol smokes passed. The superseded Vite frontend passed its checks before the Nuxt migration; Nuxt acceptance remains open.
- Nuxt lint and typecheck pass; generated Nitro routes pass HTTP, canonical, JSON-LD, health, and robots smoke checks. Production dependency audit reports zero known runtime vulnerabilities.
- After ADR-015, Nuxt lint/typecheck pass on Node 24.18.0; Python 3.14.6 Ruff, strict mypy (36 files), compilation, Alembic-head, and live UUID-version checks pass. CI YAML, lock synchronization, and matching English/Hindi catalog keys pass local validation; first remote CI run remains pending.
- ADR-016 localization JSON/registry checks pass. After correcting the CI-reported locale type boundary, the exact `npm run typecheck` command passes locally with the non-localhost CI site URL.
- The first GitHub localization run caught Vue template widening of `language.code`. The registry now derives its public language type from literal data, the component validates event input through the registry, and the CI site URL applies to every frontend step; rerun evidence remains pending.
- Docker/Compose static checks, development/production Compose interpolation, both production image builds, and isolated application-container smokes pass. Full-stack runtime critical-flow evidence remains required before the Docker acceptance checkbox can close.

## Known issues

- Production provider selection and credentials are unresolved.
- The pinned ClamAV pull succeeded after a transient TLS retry. Full-stack acceptance reached healthy PostgreSQL, Redis, MinIO, migrations, and backend plus frontend startup, then Docker Desktop returned HTTP 500 from container inspect and became unresponsive during the ClamAV health wait.
- Active deletion/retention cleanup and the final security review remain private-beta blockers.
- Real provider/storage/scanner integration and visual browser QA remain outstanding in this environment.

## Next recommended task

Complete native Windows infrastructure setup from `LOCAL_DEVELOPMENT.md`, start the full stack with `scripts/start-local.ps1`, complete visual review, and run the implemented Phase 1 flow with a trusted LibreTranslate-compatible provider.

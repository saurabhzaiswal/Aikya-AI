# Current Testing Position

Automated unit, integration, and E2E suites are temporarily deferred by explicit founder instruction during the current MVP implementation phase. This is a scheduling decision, not a quality claim.

Current mandatory verification includes frontend/backend static checks, production builds, import/config checks, Alembic migration checks, Compose configuration checks, API smoke checks, security review, and manual critical-flow checks where the environment permits.

## Phase 1 evidence - 2026-08-01

- Passed: ESLint, Vue TypeScript check, Vite production build, Ruff, strict mypy, Python compile, FastAPI OpenAPI generation, and Alembic upgrade against a disposable SQLite database.
- Passed: synthetic registration/login/current-user/dashboard, refresh rotation/logout/replay rejection, configured text translation/history, signed upload validation, readable PDF rendering/full worker job, and clamd protocol clean/infected/unavailable smoke flows.
- Passed: Compose YAML parsing, required-file audit, Markdown relative-link check, `.agents`/environment ignore check, common credential-pattern scan, Options API scan, and component color-token scan.
- Environment-limited: Docker/Compose runtime, real PostgreSQL/Redis/MinIO/Celery/ClamAV/provider integration, and visual browser QA.
- Beta-gated: automated tenant/auth/document/security suites, deletion/retention behavior, restore/recovery drill, and final security review.

Code must remain test-friendly through dependency injection, provider interfaces, deterministic domain functions, explicit transaction boundaries, and stable API contracts. The complete planned strategy is in [`10-testing.md`](10-testing.md). Before private beta, tenant isolation, authentication, document security, provider adapters, jobs, migrations, critical flows, and golden PDF fixtures require automated coverage.

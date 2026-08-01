# Architecture Decision Register

Status values: Proposed, Accepted, Superseded, Rejected

| ID | Decision | Status | Required before | Evidence/owner |
|---|---|---|---|---|
| [ADR-001](ADR-001-vue-over-react.md) | Vue 3 Options API over React | Accepted | frontend implementation | Founder |
| [ADR-002](ADR-002-fastapi-backend.md) | FastAPI backend | Accepted | backend implementation | Founder |
| [ADR-003](ADR-003-modular-monolith.md) | Modular monolith with independently scalable worker roles | Accepted | platform implementation | Founder |
| [ADR-004](ADR-004-organization-as-tenant.md) | Organization-as-tenant model with personal organizations | Accepted | identity/database implementation | Founder-approved Phase 1 scope |
| ADR-005 | Versioned canonical Document IR | Proposed | document spikes | Document Engineering |
| ADR-006 | Fidelity tiers and per-format quality thresholds | Proposed | public MVP promise | Product + QA |
| [ADR-007](ADR-007-translation-provider-boundary.md) | Provider-neutral translation boundary; deployment provider pending | Accepted | translation implementation | Founder-approved abstraction |
| [ADR-008](ADR-008-web-session-security.md) | Short access token and rotating refresh session | Accepted | identity implementation | Founder-approved Phase 1 scope |
| ADR-009 | Cloud region, storage, queue, and secrets platform | Proposed | staging | DevOps + Security |
| ADR-010 | Default retention and deletion semantics | Proposed | upload implementation | Product + Privacy |
| ADR-011 | Usage unit, reservation, settlement, and pricing model | Proposed | usage implementation | Product + Finance |
| ADR-012 | Separate marketing/dashboard rendering boundary | Rejected for Phase 1 | web implementation | Superseded by ADR-014 |
| [ADR-013](ADR-013-clamav-malware-scanning.md) | Isolated ClamAV upload scanning | Accepted for Phase 1 | PDF processing | CTO; production review pending |
| [ADR-014](ADR-014-unified-nuxt4-frontend.md) | Unified Nuxt 4 SSR/public + client/private web application | Accepted | frontend migration | Founder |

## Current architectural baseline

Until reviewed ADR files exist, the technical blueprint proposes:

- A modular FastAPI monolith with PostgreSQL and independent Celery worker processes.
- Redis as non-authoritative cache/queue infrastructure.
- Private S3-compatible binary storage.
- A unified Nuxt 4/Vue 3 web application with SSR public routes and client-rendered private routes.
- Provider adapters for translation, OCR, AI, and speech.
- Durable processing state and a transactional outbox.
- Explicit organization tenancy and immutable document/output versions.

Rows marked Proposed remain unapproved. Accepted rows have dedicated ADRs and their documented authority; production-review caveats remain binding.

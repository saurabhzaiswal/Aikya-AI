# System Architecture

Status: Accepted Phase 1 baseline; later-phase modules remain proposals  
Related decisions: ADR-001, ADR-002, ADR-003, ADR-004, ADR-007, ADR-008, ADR-013, and ADR-014

## Executive architecture

Aikya starts as a modular monolith with one transactional PostgreSQL database and independently scalable process roles. HTTP concerns, business modules, and provider abstractions share a codebase. Long-running document work is executed by document, OCR, translation, and render workers through Celery queues. Redis carries transient queue/cache/limit data; it is never the source of truth. Private S3-compatible object storage holds binaries.

Boxes labeled “Service” in the diagrams are logical backend modules unless explicitly listed as a deployable role. They are not initial network microservices.

This choice minimizes distributed transaction and deployment overhead while preserving extraction seams. A module becomes a service only when measured resource isolation, fault isolation, team ownership, release cadence, or traffic justifies the cost.

The editable system view is [`diagrams/system-architecture.excalidraw`](diagrams/system-architecture.excalidraw).

## Context

The initial client is one Nuxt 4/Vue 3 web application: public routes are SSR/SEO surfaces and private `/app/**` routes are client-rendered. Later clients may include a Vue/Vite browser extension, Capacitor mobile application, and Tauri desktop application. All use versioned HTTP contracts from the backend. Clients never call translation, AI, OCR, storage-administration, or payment-provider APIs with Aikya secrets.

At the edge, TLS, CDN, WAF controls, request-size limits, and routing protect the public application. Large files transfer directly to object storage using short-lived, least-privilege signed requests authorized by the API.

## Logical layers

| Layer | Responsibility |
|---|---|
| Clients | Presentation, local interaction state, upload/download transfer, accessible progress |
| Edge | TLS termination, static delivery, routing, basic abuse controls |
| API | Authentication, authorization, metadata, orchestration, synchronous bounded work |
| Domain modules | Business invariants and use cases |
| Job runtime | Durable stage orchestration, retries, cancellation, heartbeats |
| Processing adapters | File parsers/renderers, OCR, translation, AI, audio |
| Data platform | PostgreSQL, Redis, object storage |
| External providers | OAuth, translation, AI, speech, email, billing |
| Operations | Logs, metrics, traces, alerting, backups, secrets |

## Deployable roles

- `web`: Nuxt/Nitro SSR process behind the edge; public routes may be prerendered while private routes remain client-rendered.
- `api`: stateless FastAPI replicas for bounded operations.
- `worker-document`: validation, extraction, normalization, segmentation.
- `worker-ocr`: image preprocessing and OCR; isolated CPU/GPU pools.
- `worker-translation`: batching and translation-provider interaction.
- `worker-render`: reconstruction, font fitting, format output, quality checks.
- `scheduler`: retention, deletion, usage rollups, outbox dispatch, and stuck-job recovery, guarded by a distributed/database lock.

One backend image may supply all Python roles using different entry commands. Images are immutable and environment-neutral.

## Module map

| Module | Owned state | Public responsibility |
|---|---|---|
| Identity | identities, sessions, verification | authenticate principals and rotate/revoke sessions |
| Users | profiles and preferences | user lifecycle and locale defaults |
| Organizations | tenants, membership, teams, invitations | permission context and collaboration |
| Workspaces | workspace/folder organization | locate and share business resources |
| Documents | documents, versions, pages, segments, lineage | source lifecycle and canonical representation |
| Jobs | jobs, steps, attempts, checkpoints | state machine, cancellation, retry, progress |
| Translation | runs, translated segments, glossary, memory | detect, segment, route, translate, normalize |
| OCR | OCR runs and region confidence | extract visible text through engine adapters |
| Rendering | outputs and quality warnings | reconstruct supported formats and verify output |
| Storage | file objects and lifecycle | quarantine, signed transfer, scan, erase |
| Usage | events, reservations, rollups | authorize/measure consumption |
| Billing | plans, subscriptions, invoices | translate payment state into entitlements |
| AI | explicit enhancement runs | explain/summarize/rewrite without coupling core translation |
| Audio | speech jobs/artifacts | synthesize translated text |
| Notifications | messages/preferences/delivery | inform users without becoming job truth |
| Developer API | keys, scopes, external idempotency, webhooks | machine-to-machine access |
| Audit | append-only business/security events | accountable access/change history |
| Admin | restricted support operations | safe diagnostics and recovery |

Modules call only public application interfaces or consume versioned domain events. A module may not import another module's repositories or write its tables.

## Canonical Document IR

Document IR is the product's central technical asset. Parsers convert DOCX, PDF, images, and later formats into a versioned format-neutral representation. It preserves:

- page/container geometry, reading order, hierarchy, rotation, and z-order;
- blocks such as paragraphs, lists, tables, cells, captions, headers, and footnotes;
- text runs, protected tokens, style/font references, links, and inline boundaries;
- image/font asset references;
- stable translation-segment IDs and neighboring context;
- extraction/OCR confidence, overflow, collision, and missing-glyph warnings.

The IR schema is validated and versioned. Large representations live in object storage; queryable segment and quality metadata lives in PostgreSQL. Renderers accept a declared IR version, and migrations or compatibility adapters support retained versions.

## Processing flow

See [`diagrams/document-processing-flow.excalidraw`](diagrams/document-processing-flow.excalidraw).

1. Create upload intent after permission, type, size, quota, and concurrency preflight.
2. Upload to quarantine and complete with expected checksum/size.
3. Validate magic bytes and structure; scan for malware; reject archives/macros/external content by policy.
4. Store immutable source metadata and create a durable job in the same transaction as its outbox event.
5. Extract embedded text and layout into Document IR.
6. OCR only pages/regions without adequate embedded text.
7. Segment with protected tokens, style boundaries, context, stable hashes, and language detection.
8. Route to an allowed provider based on capability, tenant privacy policy, quality tier, health, cost, and limits.
9. Reconstruct with format-specific renderer, font fallback, fitting, and readable fallback.
10. Run automated output checks, atomically publish, settle usage, and notify.

Job states are `created`, `uploading`, `validating`, `extracting`, `ocr`, `segmenting`, `translating`, `rendering`, `quality_check`, `completed`, `failed`, `cancelled`, and `expired`. Transitions use optimistic locking or atomic conditional updates. A cancelled task checks cancellation between bounded units of work.

## Delivery and consistency

- API commands requiring durability commit business state and an outbox event together.
- The dispatcher publishes unsent events and marks them only after successful handoff.
- Consumers deduplicate using event/job/stage idempotency keys.
- Worker outputs are written to temporary object keys and promoted only after validation.
- Usage reserves estimated units and settles actual units once per billable result.
- Redis loss may delay work or invalidate cache, but cannot erase accepted job or billing truth.

## Provider boundaries

Translation, OCR, AI, speech, storage, email, OAuth, and payment adapters normalize capabilities, configuration, health, result metadata, retryability, and error codes. Provider-specific response objects do not cross the infrastructure boundary.

Translation records capture provider, adapter and model version where available, segmentation/settings/glossary versions, source hash, target locale, privacy class, usage, and timing. Fallback occurs only to providers allowed by organization policy and disclosure.

## Scalability path

1. Horizontally scale stateless API and direct binary transfer.
2. Split queues by resource profile, priority, plan, and provider.
3. Autoscale workers on queue age and saturation with hard cost bounds.
4. Batch provider work, cache only policy-safe deterministic results, and use circuit breakers.
5. Pool PostgreSQL connections, optimize/index tenant queries, partition append-only ledgers, and move reporting to replicas.
6. Add managed queue or RabbitMQ if Redis transport behavior becomes limiting.
7. Extract OCR/rendering first if resource isolation warrants it; preserve API/domain contracts.

## Failure model

Failures are classified as user-correctable, permanent unsupported, transient provider/infrastructure, policy/permission, quota, cancelled, or internal. Public errors remain content-free and include a request/job ID. Transient retries are bounded with exponential backoff and jitter. Poison work enters a dead-letter/review state without logging payload text.

## Architectural constraints

- No microservices in the initial phase.
- No shared mutable binaries or source mutation.
- No provider secret or SDK in clients.
- No long-running processing inside HTTP requests.
- No user content in observability or analytics.
- No cross-tenant cache key, object prefix, or query.
- No unversioned public event, API, IR, or pricing-entitlement contract.

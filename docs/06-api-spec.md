# API Specification

Status: Planning contract; OpenAPI artifact follows implementation  
Base path: `/api/v1`

## API goals

The API exposes resource-oriented, tenant-safe workflows to web and future clients. Large document work is asynchronous. Binary transfer uses signed object-storage requests. Public developer access will reuse application use cases but have a separately governed authentication and rate-limit surface.

## Protocol conventions

- HTTPS and JSON UTF-8 for metadata.
- ISO 8601 UTC timestamps, BCP 47 language tags, bytes for sizes, integer minor units plus currency.
- Opaque resource IDs.
- Cursor pagination with stable `next_cursor`; default and maximum page sizes are documented per collection.
- `Idempotency-Key` is required for uploads, job creation, subscription mutations, and other retryable side effects.
- `If-Match` or explicit resource version is required for collision-sensitive updates.
- Request IDs are returned and accepted from trusted gateway format only.
- Backward-compatible additive changes stay in v1; removals or semantic breaks require a new version and migration window.

## Authentication

Browser access uses a short-lived access token in memory plus rotating refresh credential in a Secure, HttpOnly cookie, or an approved opaque-session alternative. OAuth uses authorization code with PKCE. Developer API keys use a visible prefix and secret shown once, stored as a hash, and scoped by organization/capability.

Every request resolves principal, session/key status, organization context, membership, entitlement, and resource ownership. Clients cannot select arbitrary organization IDs without membership.

## Error envelope

All errors use:

- `code`: stable machine-readable identifier such as `file_type_unsupported`.
- `message`: safe localized/user-displayable fallback without sensitive content.
- `request_id`: support correlation.
- `field_errors`: optional validation details.
- `retryable`: whether repeating later may work.
- `retry_after_seconds`: optional throttling/backoff guidance.

HTTP status conveys protocol category; business/job error codes convey precise handling. Provider raw errors and document text are never returned.

## Resource groups

### Identity and sessions

| Method and path | Purpose |
|---|---|
| `POST /auth/register` | create pending/verified user according to policy |
| `POST /auth/login` | authenticate local identity and establish session |
| `POST /auth/refresh` | rotate refresh credential and issue access token |
| `POST /auth/logout` | revoke current session |
| `GET /auth/sessions` | list safe session/device metadata |
| `DELETE /auth/sessions/{session_id}` | revoke a session |
| `POST /auth/password/forgot` | issue generic recovery response |
| `POST /auth/password/reset` | consume single-use recovery token |
| `GET /auth/oauth/{provider}/start` | initiate PKCE flow |
| `GET /auth/oauth/{provider}/callback` | validate and complete flow |

Auth endpoints have stricter abuse limits and generic responses that prevent account enumeration.

### User, organization, and workspace

- `GET/PATCH /users/me`
- `GET /organizations`, `GET/PATCH /organizations/{id}`
- `GET/POST /organizations/{id}/invitations`
- `GET/PATCH/DELETE /organizations/{id}/members/{membership_id}`
- `GET/POST /workspaces`, `GET/PATCH /workspaces/{id}`
- `GET/POST/PATCH/DELETE /workspaces/{id}/folders...`

The active organization is explicit in route/resource context and validated server-side.

### Uploads and files

1. `POST /uploads` accepts intended filename, declared media type, bytes, checksum, purpose, and optional document intent. It returns upload ID, constrained signed request, expiry, and headers.
2. Client transfers bytes directly to quarantine.
3. `POST /uploads/{id}/complete` confirms transfer. Server independently verifies object attributes and creates validation work.
4. `DELETE /uploads/{id}` aborts an incomplete upload.
5. Authorized output download uses `POST /files/{id}/download-url`; raw object keys are never exposed as authorization.

### Documents

| Method and path | Purpose |
|---|---|
| `POST /documents` | bind a completed clean upload to a document |
| `GET /documents` | cursor-paginated history with safe filters |
| `GET /documents/{id}` | metadata, current version, state, expiry, warnings |
| `PATCH /documents/{id}` | rename/move/retention settings with version guard |
| `DELETE /documents/{id}` | request lifecycle deletion; returns deletion resource |
| `GET /documents/{id}/versions` | immutable lineage |
| `GET /documents/{id}/pages` | page metadata/thumbnails after authorization |

### Translation

- `POST /translation/estimate`: estimate units, cost display inputs, provider/privacy tier, and supported fidelity.
- `POST /translation/text`: synchronous only under configured length/time limits; otherwise returns a job.
- `POST /documents/{id}/translations`: create idempotent run with version, source/target tags, mode, glossary, retention, and explicit AI=false by default.
- `GET /translations/{run_id}`: status, progress, settings, usage, warnings, outputs.
- `GET /translations/{run_id}/segments`: authorized cursor-paginated comparison data.
- `POST /translations/{run_id}/cancel`: cancellation request, not a claim of immediate termination.
- `POST /translations/{run_id}/retry`: only allowed for retryable terminal runs and idempotently creates/continues approved work.

### Jobs and progress

- `GET /jobs/{id}` returns public stage, monotonic progress, timestamps, safe error, retry/cancel availability.
- `POST /jobs/{id}/cancel` requests cancellation.
- Initial clients poll using backoff and visibility-aware intervals. A later `GET /events` Server-Sent Events stream may deliver progress; PostgreSQL job state remains authoritative.

### Languages and capabilities

`GET /languages` and `GET /capabilities` return supported source/target pairs by feature, format, quality tier, script direction, and availability. Capability response is cached but provider health may temporarily narrow it.

### Usage and notifications

- `GET /usage/current`, `GET /usage/history`
- `GET /notifications`, `POST /notifications/{id}/read`
- `GET/PATCH /notification-preferences`

Usage responses distinguish included, reserved, consumed, remaining, reset, hard limit, and concurrency.

## Asynchronous semantics

Creation endpoints return `202 Accepted` with job/run resource when work is queued. A job accepted only after durable database commit. Retried requests with the same idempotency key and equivalent body return the original resource; a different body returns an idempotency conflict.

Job stage progress is advisory and monotonic; completion is authoritative only when status is `completed` and published output metadata exists. Cancellation is cooperative and may finish the current bounded operation. Usage is settled based on documented outcomes.

## Rate limiting

Return standard rate-limit information where supported and `429` with retry guidance. Policies combine IP, session/user, organization, API key, endpoint class, and concurrent jobs. Authentication, signed URL creation, expensive estimates, and translation creation use distinct buckets.

## Webhook design for developer phase

Webhooks contain event ID/type/version, creation time, organization/resource IDs, and safe status metadata—not document text or download URLs. Delivery uses HMAC signature with timestamp/replay window, exponential retries, stable event ID, endpoint disablement after sustained failure, and a delivery log. Consumers retrieve authorized details through the API.

## Compatibility and documentation

OpenAPI is generated from implementation schemas and reviewed as a public artifact. CI detects breaking changes and compiles the generated TypeScript client. Examples use synthetic data. Deprecations include announcement, response headers/documentation, migration path, metrics, and an end date.

# Database Design

Status: Logical design; physical DDL follows approved ADRs  
Database: PostgreSQL

## Design goals

The schema must make tenant ownership, immutable document lineage, durable job state, idempotent usage, and privacy lifecycle difficult to bypass. PostgreSQL is authoritative; Redis and object storage complement it but do not replace transactional state.

The editable entity overview is [`diagrams/database-er.excalidraw`](diagrams/database-er.excalidraw). That diagram is intentionally high level; this document is the source for complete logical design.

## Conventions

- Application-generated UUIDv7 identifiers for persisted entities and ordered business identifiers; never expose sequential IDs. All ORM primary-key defaults use the shared `app.platform.identifiers.new_uuid7` generator.
- UUIDv4 remains acceptable only for non-persisted security-random correlation values such as request IDs and JWT JTIs. It must not be reintroduced as an ORM primary-key default.
- `timestamptz` values in UTC; application localizes display.
- Lowercase canonical BCP 47 language tags.
- Integer monetary minor units plus ISO currency.
- `created_at`/`updated_at` on mutable entities; state-specific timestamps where operationally useful.
- Tenant tables carry non-null `organization_id`. Repository APIs require tenant scope.
- Database row-level security is added as defense in depth before shared business tenancy launches.
- JSONB only for validated, versioned, non-relational metadata.
- Secrets are hashes or secrets-manager references, never plaintext.
- Personally identifiable fields are minimized; content-free logs/audits reference opaque IDs.

## Identity and tenancy tables

### `users`

Profile identity: normalized unique email, display name, locale, timezone, status, verification/login/deletion timestamps. Email changes require verification and audit. Deactivation is distinct from erasure.

### `auth_identities`

Links a user to `local`, Google, or later identity providers using unique `(provider, provider_subject)`. Local identities hold an adaptive password hash only. OAuth tokens are avoided unless an integration needs them; unavoidable tokens are encrypted and separately scoped.

### `sessions`

Holds refresh-token family/hash, user, issued/expiry/revocation timestamps, rotation lineage, and bounded device/security metadata. Raw refresh tokens are never stored.

### `organizations`

The tenant boundary. Fields include type (`personal`, `business`), name, slug, status, and data region. Every user starts with a personal organization.

### Membership and collaboration

- `organization_memberships`: organization, user, fixed role, state, invitation/acceptance metadata; unique organization-user pair.
- `teams`: organization-owned named group.
- `team_memberships`: membership-to-team link and team role.
- `invitations`: email, proposed role, token hash, expiry, acceptance/revocation; only one active equivalent invitation.
- `workspaces`: organization, name, visibility, creator.
- `workspace_memberships`: optional additional workspace restriction.
- `user_preferences` and `organization_settings`: validated settings including locale, translation defaults, provider policy, and retention policy.

## Document and storage tables

### `file_objects`

Metadata for private object-storage binaries: organization, purpose, provider, bucket, randomized key, MIME, extension, byte length, SHA-256 checksum, encryption key reference, scan/lifecycle states, expiry/deletion timestamps. Object key and checksum/purpose rules prevent accidental collisions. No file bytes are stored in PostgreSQL.

### `documents`

User-facing logical document: organization, workspace, folder, creator, title, kind, source language, lifecycle state, retention policy, and expiry. A document remains stable while versions and outputs are immutable children.

### `document_versions`

Document, monotonically increasing version number, source file, IR artifact, parser/schema versions, page count, source checksum, lineage/action. Unique `(document_id, version_no)`.

### `document_pages`

Version, zero-based page index, dimensions, rotation, thumbnail, extraction state, page confidence. Unique version-page pair.

### `document_segments`

Stable segment key within version, page/container/parent, block kind, reading order, source text, normalized source hash, language, geometry/style JSON, extraction method, and confidence. Full text is authorized content and excluded from ordinary logs, indexes, and analytics.

### `rendered_outputs`

Translation run, output format/file, renderer and IR versions, fidelity tier, quality score, warnings, creation/expiry. Publish only after object verification and transactional status update.

### Lifecycle tables

- `folders`: adjacency hierarchy with cycle prevention and scoped sibling names.
- `deletion_requests`: actor, target, reason, state, schedule, attempts, and completion evidence.
- `sharing_links` later: token hash, resource, permissions, expiry, revocation; disabled until threat-reviewed.

## Processing tables

### `processing_jobs`

Organization, target resource, type, state, progress, priority, requester, idempotency key, timestamps, heartbeat, retry/error classification, cancellation request, and concurrency version. Unique `(organization_id, requester_scope, idempotency_key)` where present.

### `job_steps`

Job, stage, attempt, state, worker correlation ID, start/finish/heartbeat, checkpoint artifact, safe error code/metadata. Unique job-stage-attempt. Progress is monotonic within an attempt.

### `ocr_runs`

Version/page scope, engine/version, language hints, settings hash, state, region count, aggregate confidence, resource usage, timing. OCR region details map to segments or a versioned IR artifact.

### `outbox_events`

Aggregate type/id, event type, schema version, content-free payload, creation, publish lease, attempts, and published timestamp. Indexed for unpublished rows. Consumers keep their own durable deduplication record or use stage uniqueness.

## Translation, AI, and audio tables

- `languages`: BCP 47 tag, English/native names, script, direction, active status.
- `provider_capabilities`: provider/capability, language pair, tier, privacy classification, limits, effective period.
- `translation_runs`: document version or bounded text request, source/target tags, mode, provider/adapter/model/segmenter/glossary versions, settings hash, state, estimate and actual usage, quality summary.
- `translated_segments`: run, source segment, target text, status, source hash, provider reference, confidence/quality fields; unique run-source segment.
- `glossaries` and `glossary_entries`: organization-private, versioned terminology and match rules.
- `translation_memory_entries`: organization-private source/target/context hash, text, provenance, quality, usage time. Not enabled until retention and deletion semantics are approved.
- `ai_runs`: explicit action, source version, provider/model/prompt-template versions, consent/privacy mode, usage, status, output reference.
- `audio_runs`: source resource, locale, voice/provider/settings, usage, state, output file.

AI output is always a separate version/action; it never overwrites translation or source.

## Usage, billing, and API tables

- `plans`: immutable versioned plan definitions with effective dates.
- `plan_entitlements`: feature key, limit, unit, cadence, concurrency/quality controls.
- `subscriptions`: organization, provider customer/subscription references, plan version, state, billing period and cancellation timestamps.
- `billing_events`: unique provider event ID, signature result, receipt/process states, safe payload reference.
- `invoices` and `payments`: provider references, amount, currency, status; no payment instrument data.
- `usage_events`: append-only organization/feature/unit/quantity/resource/actor/idempotency record.
- `usage_rollups`: reproducible period aggregates for display and fast checks.
- `quota_reservations`: estimated units held for a job and later settled/released.
- `api_keys`: visible prefix, secret hash, scopes, creator, expiry/revocation/last-used.
- `webhook_endpoints` and `webhook_deliveries`: encrypted signing-secret reference, allowlisted URL policy, events, attempts, backoff, response status.

## Trust and communication tables

- `notifications`: user/organization, message key and safe parameters, resource reference, read/delivery state.
- `notification_preferences`: user/channel/event choices.
- `audit_events`: append-only actor/action/target/outcome/request ID and redacted security context.
- `idempotency_records`: actor scope, key, request hash, response reference/status, expiry.
- `feature_flags`: environment and organization targeting with validated config.

## Critical constraints

- No document/file/translation row without an organization.
- Cross-table tenant identity must match; enforce through composite foreign keys where complexity remains manageable and test all paths regardless.
- Membership uniqueness and last-owner protection occur transactionally.
- Published outputs reference clean, active file objects.
- Completed usage settlement is exactly once per reservation/job.
- A translation segment belongs to the same version/tenant as its run.
- Deletion state is monotonic unless a separately audited recovery workflow exists.
- Billing events, usage events, and audit events are immutable to application roles.

## Index plan

- User email and provider-subject unique indexes.
- `(organization_id, workspace_id, created_at desc, id)` for document history.
- `(organization_id, lifecycle_status, expires_at)` for retention.
- `(state, queue, priority, created_at)` and `(state, heartbeat_at)` for jobs/recovery.
- `(document_version_id, reading_order)` and stable segment lookup.
- `(organization_id, feature, occurred_at)` for usage; partition-ready monthly.
- `(organization_id, occurred_at)` for audit; partition-ready monthly.
- Unpublished outbox partial index.
- API-key prefix lookup plus constant-time hash verification.

Do not add full-text document indexes until search requirements, encryption, deletion, and privacy are designed.

## Migration and backup policy

Migrations are forward-only in production and follow expand/migrate/contract. Destructive column/table removal waits until all deployed versions stop using it and data retention/legal requirements permit removal. Large backfills are resumable jobs, not blocking transactions.

Production backups are encrypted, access-controlled, monitored, and restored in drills. RPO/RTO and backup expiry are documented per environment. Customer deletion removes active data promptly and ages out of backups according to the disclosed schedule.

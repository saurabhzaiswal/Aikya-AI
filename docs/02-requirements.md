# Product and System Requirements

Status: Foundation baseline  
Requirement notation: `FR` functional, `NFR` non-functional, `SEC` security/privacy

## Scope and release definitions

The private-beta MVP is the web application plus the services required to translate plain text, DOCX, digital PDFs, images, and a bounded class of scanned PDFs. Later capabilities remain architectural requirements but are not launch commitments.

Priorities use Must, Should, Could, and Later. A Must requirement blocks release. Requirements are accepted only through observable criteria, not implementation completion.

## Personas and jobs

| Persona | Primary job | Critical concern |
|---|---|---|
| Individual reader | Understand a foreign-language document | accuracy, speed, simple export |
| Professional | Translate a structured business document | layout and terminology |
| Job seeker | Translate a resume | ATS-safe formatting |
| Researcher/student | Read and compare source material | traceability and side-by-side review |
| Organization admin | Manage people, usage, privacy, and spend | control and auditability |
| Developer | Integrate language workflows | stable API, limits, observability |

## MVP functional requirements

### Identity, tenancy, and workspace

- **FR-001 Must:** A user can register, verify an email address, sign in, refresh a session, sign out, recover a password, and revoke active sessions.
- **FR-002 Must:** Google OAuth is supported through Authorization Code + PKCE. Additional social providers require demand evidence.
- **FR-003 Must:** Every new user receives a personal organization and workspace.
- **FR-004 Must:** Every document, file, job, translation, usage event, and output has an explicit organization owner.
- **FR-005 Must:** Owners can invite and remove members once shared organizations are enabled; role checks apply server-side.
- **FR-006 Should:** Users can choose UI locale, theme, source language default, target language default, and retention preference.

### Upload and storage

- **FR-020 Must:** Users can upload supported files directly to private object storage through a short-lived signed request.
- **FR-021 Must:** The server validates entitlement, file size, MIME signature, extension, checksum, page count, archive behavior, and malware status before processing.
- **FR-022 Must:** Source files are immutable. Every transformation creates a versioned derived artifact.
- **FR-023 Must:** Users can cancel processing and delete documents, subject to clear lifecycle states.
- **FR-024 Must:** Temporary documents expire automatically according to the configured policy.
- **FR-025 Should:** Failed uploads can resume where storage-provider support and integrity controls allow it.

### Translation and processing

- **FR-040 Must:** Users can translate bounded plain text and receive detected language, target text, provider-neutral status, and usage.
- **FR-041 Must:** Users can request document translation with explicit source or automatic detection and one target locale.
- **FR-042 Must:** Document processing exposes durable state, stage progress, retryability, cancellation, and safe user-facing error codes.
- **FR-043 Must:** DOCX extraction and reconstruction preserve supported paragraphs, runs, lists, tables, headers/footers, links, and images within the published fidelity contract.
- **FR-044 Must:** Digital PDF processing preserves page count and text regions when confidence permits, with overflow and font warnings.
- **FR-045 Must:** Image and scanned PDF processing records OCR confidence and uses a readable fallback below the fidelity threshold.
- **FR-046 Must:** All translation/OCR providers are accessed through internal adapters and normalized capability/error contracts.
- **FR-047 Must:** AI enhancement is not invoked during basic translation unless the user explicitly requests it.
- **FR-048 Should:** Users can view original and translated segments side by side.
- **FR-049 Should:** A user can retry a failed retryable stage without duplicating usage or outputs.

### Results and history

- **FR-060 Must:** Users can preview job results, warnings, source/target languages, format, size, and creation/expiry timestamps.
- **FR-061 Must:** Users can download an authorized output through a short-lived URL.
- **FR-062 Must:** The dashboard lists documents with cursor pagination and filters by state, language, format, and date.
- **FR-063 Must:** Output quality checks validate readability, non-empty content, page count, target-language presence, glyph coverage, and overflow signals.
- **FR-064 Should:** Users can save, rename, move, favorite, or delete a document.

### Usage and notifications

- **FR-080 Must:** Usage is measured through an immutable idempotent event ledger.
- **FR-081 Must:** Large jobs reserve estimated quota before processing and settle against actual units afterward.
- **FR-082 Must:** Users see current allowance and an actionable error when a hard limit is reached.
- **FR-083 Should:** In-app and email notifications announce completion or actionable failure without including document text.

## Later functional requirements

- Browser extension: translate selection/page text without altering application logic or collecting unrelated page content.
- Resume workflow: translate and optionally improve a resume while keeping separate original, translation, and enhancement versions.
- AI workspace: explain, summarize, rewrite, and grammar actions with explicit intent and provider disclosure.
- Audio: synthesize translated content with locale/voice selection and accessible playback.
- Developer API: scoped API keys, idempotency, rate limits, webhooks, SDKs, and developer documentation.
- Mobile/live camera: consent-aware camera capture, bounded frame processing, OCR overlays, thermal/battery/network budgets.
- Enterprise: SSO, SCIM, custom retention, audit export, data residency, private connectivity, and deployment options.

## Non-functional requirements

### Performance and capacity

- **NFR-001:** Metadata endpoints target p95 below 300 ms at supported beta load, excluding third-party calls and binary transfer.
- **NFR-002:** Upload/download data travels directly between client and object storage whenever practical.
- **NFR-003:** Job stage progress remains fresh at transitions and bounded heartbeat intervals.
- **NFR-004:** Each parser/worker has enforced file, memory, CPU, duration, and decompression limits.
- **NFR-005:** Capacity tests model file-size, format, page-count, OCR, language, and provider mixes rather than request rate alone.

### Reliability

- **NFR-020:** Accepted jobs are durably recorded before acknowledgement.
- **NFR-021:** At-least-once task delivery cannot create duplicate charges, translation segments, or published output.
- **NFR-022:** Provider timeouts, rate limits, and temporary failures use bounded retries, circuit breakers, and normalized status.
- **NFR-023:** Beta availability target is 99.5% monthly; proposed beta RPO is 24 hours and RTO is 4 hours.
- **NFR-024:** Backup restoration, deletion, and worker-recovery procedures are exercised before public launch.

### Maintainability and portability

- **NFR-040:** Backend modules enforce explicit ownership and dependency boundaries.
- **NFR-041:** Domain logic is independent of FastAPI, SQLAlchemy, Celery, and vendor SDKs.
- **NFR-042:** OpenAPI generates typed client contracts; breaking compatibility fails CI.
- **NFR-043:** Environments use immutable containers and validated configuration, with no manual runtime dependency installation.
- **NFR-044:** Database migrations follow expand/migrate/contract and tolerate rolling deployment.

### Accessibility and localization

- **NFR-060:** Customer workflows target WCAG 2.2 AA.
- **NFR-061:** All actions are keyboard accessible with visible focus and semantic announcements for processing updates.
- **NFR-062:** UI copy is externalized; locale, script direction, dates, numbers, plurals, and language names are localized.
- **NFR-063:** Layouts support RTL and text expansion without clipping at common viewport sizes.

### Observability

- **NFR-080:** Requests and jobs carry correlation identifiers through the API, outbox, workers, storage, and provider calls.
- **NFR-081:** Logs, traces, metrics, and analytics contain no document text, access token, password, API secret, or signed URL.
- **NFR-082:** Dashboards cover API health, queue age, job outcomes, stage duration, provider reliability/cost, quality warnings, quota mismatches, and deletion backlog.

## Security and privacy requirements

- **SEC-001:** TLS in transit and provider-managed encryption at rest are mandatory in production.
- **SEC-002:** Authorization validates tenant and resource permission within the application use case, not only the HTTP layer.
- **SEC-003:** Web refresh tokens are rotating, hashed server-side, and transmitted only through secure HttpOnly cookies; long-lived bearer tokens are not stored in browser local storage.
- **SEC-004:** Untrusted documents are quarantined, scanned, structure-validated, and processed in resource-limited isolated containers with restricted egress.
- **SEC-005:** Signed object URLs are short lived, least privilege, and issued only after database ownership checks.
- **SEC-006:** External provider processing and retention terms are disclosed. User content is never used for Aikya model training.
- **SEC-007:** Deletion covers active source, intermediate, output, cache, and index copies; backup expiry behavior is disclosed.
- **SEC-008:** Secrets reside in a secrets manager or development-only environment file, never in source control or images.
- **SEC-009:** Audit records are append-only and content-free; privileged support access requires reason capture and step-up controls.
- **SEC-010:** Rate limits apply by IP, user, organization, API key, and concurrent job class.

## MVP acceptance matrix

Release approval requires:

- Tenant-isolation and authorization-negative tests pass.
- The supported format/language benchmark meets approved extraction, translation, and rendering thresholds.
- Duplicate delivery, worker termination, provider outage, and failed-deletion tests recover safely.
- Accessibility and RTL checks pass for signup, upload, progress, result, export, and deletion.
- No critical or high unresolved security issue.
- Restore and incident-response exercises are complete.
- Product copy accurately describes fidelity, provider processing, retention, and AI behavior.

## Open product decisions

The first market/data region, language pairs, provider consent model, scanned-PDF launch status, default retention, file/page limits, collaboration scope, and billing launch must be resolved during Phase 0 and recorded as decisions.

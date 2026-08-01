# Testing and Quality Strategy

Status: Foundation quality plan

## Quality model

Aikya quality has four independent dimensions: semantic translation, source extraction/OCR, document reconstruction, and platform trust. A good translation in a corrupted file is a failed job; a beautiful output with wrong meaning is also failed. Release decisions use a balanced scorecard.

## Test layers

### Unit

Test domain policies, state transitions, tenant permissions, language normalization, protected-token segmentation, provider routing, quota reservation/settlement, retry classification, expiry, and quality scoring. Units are deterministic and do not require network services.

### Integration

Test PostgreSQL repositories and constraints, migrations, transaction/outbox behavior, Redis/Celery delivery assumptions, object-storage signing/lifecycle, session rotation, and adapter serialization against disposable Docker dependencies.

### Provider contract

Every translation, OCR, storage, AI, speech, email, OAuth, and billing adapter runs a common conformance suite. It validates capability declaration, language normalization, batching/limits, timeout/cancellation behavior, retry mapping, usage extraction, privacy-safe errors, and deterministic fixtures where vendor sandboxes permit.

Live provider tests are scheduled/controlled, cost-capped, and never use customer data. Pull-request tests use fakes or approved recordings scrubbed of secrets/content.

### API contract

Validate OpenAPI, request/response/error schemas, authentication, tenant authorization, cursor pagination, idempotency equivalence/conflict, optimistic concurrency, rate limits, and backward compatibility. Generated TypeScript clients must compile and pass smoke use.

### Pipeline golden tests

Maintain licensed or synthetic fixtures across:

- formats and versions;
- digital/scanned/corrupt documents;
- simple/multi-column/table-heavy/form-heavy layouts;
- Latin, Devanagari, Arabic/RTL, CJK, combining marks, emoji, and mixed scripts;
- long expansion/contraction, font gaps, rotated pages, headers/footers, links, lists, images;
- file/page/resource boundaries and malicious constructs.

Expected artifacts include extracted text, reading order, structure, segments, protected tokens, page count, warnings, target-language presence, and rendered screenshots. Fixtures have provenance/license metadata and contain no customer information.

### Visual regression

Render source and output to images at controlled settings. Measure clipping, overflow, collisions, unexpected displacement, missing glyphs, image/table loss, and page changes. Automated signals select pages for human review; pixel similarity alone cannot judge correct translation expansion.

### End-to-end

Cover signup/login, upload, preflight, processing progress, background navigation, cancellation, retry, partial success, comparison, export, expiry/deletion, quota blocking, and session revocation. Run primary flows with keyboard and representative screen readers.

### Security and resilience

- Cross-tenant permission matrix for every resource/action.
- Token theft/replay, OAuth state/nonce, CSRF/CORS, API-key scope, signed URL expiry.
- Malware, path traversal, XXE, archive bombs, active content, corrupt files, parser resource exhaustion.
- Duplicate task/event, worker kill, Redis restart, provider timeout/rate limit, partial object upload, database failover/reconnect, failed deletion.
- Billing webhook forgery/replay/out-of-order events and usage double-settlement.

### Performance

Model workload dimensions: format, bytes, pages, embedded text, OCR proportion, resolution, language pair, provider, render tier, concurrency, and organization distribution. Track API latency, queue age, time per stage, CPU/memory, provider throughput, database connections/query latency, object egress, and unit cost.

## Quality scorecard

Phase 0 defines thresholds per format/language class for:

- Extraction text accuracy and reading-order accuracy.
- OCR character/word error rate and region confidence calibration.
- Translation human assessment for adequacy, fluency, terminology, protected tokens, numbers, and names.
- Reconstruction structure retention, page/element preservation, overflow/collision, glyph coverage, and readability.
- End-to-end completion, retry, cancellation, and deletion correctness.

No single global “accuracy percentage” is published. Results are segmented by the cases users actually encounter.

## Test data policy

Use synthetic, generated, public-domain, or explicitly licensed fixtures. Never copy production/customer documents into local, CI, staging, support tickets, or vendor tests. Secrets and provider responses are sanitized before recording. Test storage has lifecycle cleanup.

## CI gates

Pull requests require formatting, linting, static types, unit tests, architecture-boundary tests, migration checks, contract compatibility, dependency/secret scans, and a bounded pipeline smoke set. Main/release adds full integration, golden/visual, image scans, SBOM, staging E2E, accessibility, and security smoke tests.

Flaky tests are defects: quarantine is time-bound, owned, and visible. A retry cannot turn a failing release gate into a pass without diagnosis.

## Manual and exploratory review

Human reviewers inspect translation meaning, difficult layouts, error/help copy, privacy disclosure, mobile/RTL behavior, and assistive technology. Native speakers review launch language pairs. Results and known limitations are captured in the release evidence.

## Defect severity

- Critical: cross-tenant exposure, secret compromise, destructive data loss, payment corruption, or broadly unusable production path.
- High: major security bypass, silent wrong/corrupt output, unrecoverable job class, inaccessible critical journey.
- Medium: visible limited-scope failure with workaround.
- Low: cosmetic or minor usability issue without material outcome impact.

No critical/high known defect ships. Security severity may override product categorization.

## Release evidence

Each release records immutable image digests, migration version, test/scan summaries, supported format/language matrix, quality benchmark changes, known limitations, feature flags, dashboard links, rollback plan, and approver. Quality regression beyond threshold blocks promotion even when all code-level tests pass.

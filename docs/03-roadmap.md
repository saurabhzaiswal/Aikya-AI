# Product and Engineering Roadmap

Status: Proposed sequencing baseline  
Planning model: outcome-based gates, not fixed-date promises

## Planning principles

- Validate document quality and provider economics before building broad platform features.
- Ship complete vertical slices with security, failure recovery, telemetry, and deletion—not disconnected layers.
- Protect the web MVP from extension/mobile/desktop scope.
- Use quality gates and evidence to enter the next phase.
- Dates are recalibrated after spikes. Estimates assume 3–5 experienced contributors; a solo developer should expect a materially longer schedule.

## Phase 0 — Product and feasibility validation (2–3 weeks)

Outcome: Aikya has a defensible, measurable MVP promise.

Deliverables:

- MVP PRD, user journeys, format/language matrix, non-goals, and quality scorecard.
- Licensed or synthetic golden-document corpus.
- DOCX, digital PDF, and scanned PDF/OCR reconstruction spikes.
- Two-provider translation comparison for quality, privacy, latency, availability, and cost.
- Document IR v1, provider contracts, threat model, retention proposal, and initial ADRs.
- Unit economics model per character/page and operational capacity estimate.

Gate: representative outputs meet the approved baseline, and weak format/language combinations are removed from the launch claim.

## Phase 1 — Engineering platform foundation (2–3 weeks)

Outcome: A secure, observable platform can accept work without implementing the full document feature.

Deliverables:

- Repository governance, containerized local environment, CI, staging, secrets/configuration policy.
- Identity, personal organizations, workspaces, and RBAC baseline.
- Private upload quarantine, validation/scanning, object metadata, and retention lifecycle.
- Durable job/outbox state, retries, cancellation, and worker heartbeat recovery.
- Telemetry, dashboards, alert routing, backup and recovery runbooks.

Gate: tenant-isolation tests, migration tests, upload security, job recovery, and deletion behavior pass.

## Phase 2 — Text translation vertical slice (1–2 weeks)

Outcome: users receive real value through a complete, metered translation workflow.

Deliverables:

- Provider capability registry and adapter contract.
- Language detection, estimates, routing, fallback, and normalized errors.
- Plain-text UI, history, usage reservation/settlement, and content-safe telemetry.
- Contract, provider, quota, accessibility, and failure tests.

Gate: target language pairs meet quality/latency thresholds and usage reconciles under duplicate/retry tests.

## Phase 3 — DOCX document translation (3–4 weeks)

Outcome: supported DOCX files return useful translated documents with measured structural fidelity.

Deliverables:

- DOCX parser, IR mapping, segmentation, renderer, and immutable version lineage.
- Lists, tables, images, links, headers/footers, styles, font fallback, and overflow warnings.
- Result preview, side-by-side review, and safe download.
- Golden and visual regression suite.

Gate: benchmark corpus meets approved fidelity thresholds; no source mutation or silent loss.

## Phase 4 — PDF and OCR translation (4–6 weeks)

Outcome: digital and scanned documents have distinct, honest, usable workflows.

Deliverables:

- Digital PDF extraction, reading-order inference, and visual reconstruction.
- Image preprocessing, scanned-page detection, selective OCR, region confidence.
- Overlay and readable fallback renders with page-level quality warnings.
- Isolated parser/renderer runtime and hostile-file resilience tests.

Gate: separate digital/scanned acceptance thresholds pass; low-confidence output is visible and actionable.

## Phase 5 — Private beta hardening (2–3 weeks)

Outcome: selected customers can use the web product safely with supportable operations.

Deliverables:

- Onboarding, dashboard, history, retry/cancel, retention/deletion, responsive and RTL experience.
- Provider outage, queue saturation, load, restore, incident, and deletion drills.
- Privacy and terms copy, support/admin workflow, analytics, and feedback instrumentation.

Gate: critical journeys pass end to end, no critical/high security defects remain, and operators can diagnose and recover common failures.

## Phase 6 — Fidelity and format expansion

Prioritize by observed demand and benchmark readiness: PPTX, XLSX, HTML, Markdown, and EPUB; better font handling; tables; batch processing; glossary and private translation memory.

## Phase 7 — Comparison and resume intelligence

Build side-by-side and change highlighting on segment/version lineage. Treat resume translation and AI improvement as separate versions to preserve user trust and ATS-safe source structure.

## Phase 8 — Browser extension

Ship selection translation before full-page translation. Use least host permission, explicit activation, isolated content scripts, DOM mutation handling, and content minimization. Firefox support follows Chromium compatibility validation.

## Phase 9 — Monetization

Introduce versioned plan entitlements, metered usage, invoices, webhook reconciliation, and customer-facing limits. Avoid “unlimited” claims; communicate fair-use and concurrency limits.

## Phase 10 — Optional intelligence and accessibility

Add explicit AI explain/summarize/rewrite actions and text-to-speech. Record provider/model/prompt versions and show when content leaves Aikya infrastructure.

## Phase 11 — Developer and enterprise platform

Add scoped API keys, webhooks, SDKs, developer portal, separate SLOs, SSO/SCIM, audit export, custom retention, data residency, and private deployment according to signed customer requirements.

## Phase 12 — Mobile, live camera, desktop, and offline

Validate camera latency, privacy, network, battery, and thermal behavior before choosing server versus on-device processing. Tauri + Vue is the preferred desktop direction; a Vue-based Capacitor/Quasar client is the mobile direction. Offline/private models require a defined customer and update/security model.

## Cross-phase workstreams

- Security/privacy threat model and provider review.
- Document quality corpus and regression scorecard.
- Accessibility, localization, and RTL.
- Unit economics, provider health, and cost controls.
- Documentation, ADRs, support playbooks, and customer disclosures.
- Developer experience, CI duration, dependency hygiene, and release safety.

## Roadmap metrics

Each phase tracks an outcome rather than feature count: successful-job rate, correction effort, fidelity pass rate, p95 stage duration, cost per unit, retry/duplicate behavior, retained usage, and support burden. A phase is not complete because code merged; it is complete when its gate is demonstrated in staging with representative fixtures.

# Observability Plan

## Goals

Detect user impact, diagnose work without reading private content, measure quality/cost, and give a solo founder actionable alerts.

## Signals

- Structured logs: service, environment, version, request/job/tenant surrogate IDs, event, safe error code.
- Metrics: API rate/errors/latency, queue age/depth, stage duration/outcome, database/Redis/storage health, provider latency/error/cost, PDF quality warnings, auth abuse, deletion backlog.
- Traces: API to outbox/job, worker stages, storage, and provider calls with payload capture disabled.
- Product events: activation, completed translation, export, retry/cancel, retention action, and plan boundary without document content.

## Safety

Never record document text, translation output, passwords, tokens, API keys, cookies, signed URLs, provider bodies, or sensitive filenames. Scrub request headers/bodies/query strings in logs and error tracking. Use access-controlled retention and deletion policies.

## Initial dashboards and alerts

Start with API health, authentication failures, queue age, job completion/failure, provider health/cost, database capacity, storage errors, and deletion backlog. Alert on sustained user impact or SLO burn, not isolated exceptions. Every alert links a runbook.

## Implementation order

Phase 1 uses content-safe structured logs, request/job correlation, health endpoints, and core counters. Error tracking and OpenTelemetry exporters remain configuration-driven. Full dashboards/alerts are completed before private beta.

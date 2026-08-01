# ADR-003: Begin with a Modular Monolith

Date: 2026-08-01  
Status: Accepted  
Decision authority: Founder

## Context

Aikya has broad long-term scope but is operated by a solo founder. Microservices would add deployments, network failure, distributed consistency, tracing, secrets, and operational overhead before load or team boundaries justify them.

## Options considered

1. Modular monolith with independently scalable process roles.
2. Microservices per domain.
3. Unstructured single application.

## Decision

Use one modular FastAPI codebase and PostgreSQL transaction boundary. Run API, scheduler, and workload-specific Celery workers as separate containers/processes from the same backend image. Modules own their domain/table/application boundaries and communicate through public interfaces or versioned events.

## Reason

This preserves simplicity and transactional correctness while allowing CPU/GPU-heavy workers to scale independently and keeping credible future extraction seams.

## Consequences

- Logical “services” in diagrams are initially modules, not network services.
- Module-boundary checks and ownership discipline are mandatory.
- PostgreSQL remains authoritative and the transactional outbox bridges async delivery.
- Extraction requires a new ADR and measurable need such as resource/fault isolation, scale, release cadence, or team ownership.

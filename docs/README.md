# Aikya AI Documentation

This directory is the authoritative engineering and product foundation for Aikya AI. Read it before implementation or architectural change.

For a ten-second operational view, read [PROJECT_STATUS](PROJECT_STATUS.md), then the authoritative [project progress tracker](project-progress.md).

## Reading order

1. [Product vision](01-product-vision.md) - mission, users, differentiation, and boundaries.
2. [Requirements](02-requirements.md) - traceable functional, quality, and security requirements.
3. [Roadmap](03-roadmap.md) - phased outcomes and release gates.
4. [Architecture](04-architecture.md) - system topology, module boundaries, and processing design.
5. [Database](05-database.md) - tenant model, tables, constraints, indexes, and lifecycle.
6. [API specification](06-api-spec.md) - resource contracts, conventions, and errors.
7. [UI/UX](07-ui-ux.md) - design system, page model, flows, responsive behavior, and accessibility.
   - [Frontend memory safety](frontend-memory-safety.md) - lifecycle ownership, cleanup, profiling, and leak release gate.
8. [Security](08-security.md) - threat model, control baseline, and privacy lifecycle.
9. [Deployment](09-deployment.md) - environments, Docker, CI/CD, operations, and recovery.
   - [Root runbook](../RUNBOOK.md) - exact laptop, production-reference, rollback, and CI commands.
10. [Testing](10-testing.md) - test layers, fixture strategy, and release gates.
11. [Business model](11-business-model.md), [pricing](12-pricing.md), and [brand](13-brand-guidelines.md).

Founder and governance context: [founder profile](00-founder-profile.md), [project ownership](00-project-ownership.md), [founder roadmap](founder-roadmap.md), [future ideas](future-ideas.md), [observability](observability.md), and [backup/recovery](backup-recovery.md). Proprietary licensing and pre-launch legal drafts live under [`legal/`](legal/). Phase-specific contracts live under [`api/`](api/) and [`features/`](features/).

The original [technical blueprint](01-technical-blueprint.md) is retained as the source synthesis. The numbered documents decompose and refine it; when a contradiction appears, create an ADR and update both the relevant focused document and its links.

Cross-cutting implementation guidance includes [localization architecture](localization.md), [frontend memory safety](frontend-memory-safety.md), and [Docker build optimization](docker-optimization.md).

Cross-cutting implementation guidance includes [localization architecture](localization.md) and [frontend memory safety](frontend-memory-safety.md).

## Diagrams

Editable Excalidraw sources live in [`diagrams/`](diagrams/). They are architecture sources, not decorative exports. Update the `.excalidraw` file when the design changes; generated PNG/SVG files must never become the only source.

## Decision process

Significant choices use Architecture Decision Records under [`decisions/`](decisions/). A decision is significant when it affects security, data ownership, public contracts, deployment, provider lock-in, cost model, or multiple modules.

1. Copy the ADR template described in the decisions README.
2. State context and constraints before options.
3. Compare credible alternatives and consequences.
4. Assign status: Proposed, Accepted, Superseded, or Rejected.
5. Link requirements and affected docs.
6. After approval, update implementation plans and diagrams.

Decisions are append-only history. Supersede an ADR rather than silently rewriting why a choice was made.

## Documentation standards

- Owners review documents when relevant behavior changes and at least before each release.
- Use stable requirement IDs and link acceptance tests to them.
- Describe failure, privacy, accessibility, retention, operations, and rollback-not only happy paths.
- Do not include real secrets, credentials, customer data, signed URLs, or confidential provider payloads.
- Examples must be synthetic and safe to publish internally.
- Claims about availability, compliance, quality, and pricing require evidence and approval.

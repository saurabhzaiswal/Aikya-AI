# Architecture Decision Records

ADRs preserve the context, alternatives, and consequences behind significant technical decisions.

## Naming

Use `NNNN-short-kebab-title.md`, starting at `0001`. IDs are never reused.

## Template

Each ADR contains:

- Title, status, date, owners, and related requirement IDs.
- Context and constraints.
- Decision.
- Options considered.
- Positive and negative consequences.
- Security, privacy, cost, migration, and operability impact.
- Validation evidence and review date.
- Links to superseded/superseding records.

## Workflow

1. Author marks the ADR Proposed.
2. Product, engineering, security/privacy, and operations review as relevant.
3. The accountable owner marks it Accepted or Rejected.
4. Implementation links the ADR in pull requests and documentation.
5. A later change creates a new ADR and marks the prior record Superseded.

Minor local implementation details do not require ADRs. Cross-module contracts, tenant/data models, infrastructure providers, authentication, retention, and quality promises do.

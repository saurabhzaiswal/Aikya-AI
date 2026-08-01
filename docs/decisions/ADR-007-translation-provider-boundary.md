# ADR-007: Use a Provider-Neutral Translation Boundary

Date: 2026-08-01  
Status: Accepted for Phase 1 contract  
Decision authority: Founder-approved provider abstraction requirement

## Context

Translation quality, privacy terms, availability, supported languages, and cost vary by provider. Client or domain coupling to a vendor would make evaluation and migration expensive.

## Options considered

1. Internal translation contract with replaceable server-side adapters.
2. Direct provider SDK calls throughout the backend.
3. Browser-to-provider integration.

## Decision

Expose one internal provider-neutral result/error contract. Phase 1 includes a configurable LibreTranslate-compatible HTTP adapter. URLs and keys remain server-side, and raw provider responses do not cross the adapter.

## Reason

This provides a small working integration without selecting a permanent production vendor or leaking provider details into the client and domain records.

## Consequences

- A trusted real deployment provider and its privacy/retention review remain unresolved.
- New providers implement the internal contract and require capability/error verification.
- Provider failures use content-safe normalized errors.
- No automatic cross-provider fallback is enabled in Phase 1.

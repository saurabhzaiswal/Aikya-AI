# ADR-008: Use Short-Lived Access Tokens and Rotating Refresh Sessions

Date: 2026-08-01  
Status: Accepted for Phase 1  
Decision authority: Founder-approved authentication scope

## Context

The Vue application needs a secure browser session that supports revocation without storing a long-lived bearer credential in browser storage.

## Options considered

1. Short-lived bearer access token in memory plus rotating HttpOnly refresh cookie.
2. Long-lived JWT in local storage.
3. Server session cookie for every API request.

## Decision

Issue a 15-minute HS256 access token held only in memory. Store only SHA-256 hashes of opaque refresh tokens in PostgreSQL, rotate on use, revoke the token family on replay, and send refresh tokens in an HttpOnly, SameSite=Lax, path-scoped cookie that is Secure in production. Passwords use Argon2id.

## Reason

This bounds bearer exposure, supports server-side revocation and replay response, and keeps long-lived credentials out of JavaScript-readable storage while remaining manageable for a solo founder.

## Consequences

- Page reload performs one cookie-backed refresh.
- Production requires a unique secret from a secret manager and HTTPS.
- Key rotation, CSRF review, concurrent refresh behavior, and automated abuse tests are required before beta.
- An asymmetric token scheme may be reconsidered if independent token verifiers are introduced.

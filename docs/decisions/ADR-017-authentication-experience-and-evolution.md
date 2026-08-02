# ADR-017: Authentication Experience and Evolution

Status: Accepted and implemented for Google OAuth and WebAuthn Phase 1 scope
Date: 2026-08-02  
Decision owner: Saurabh Choudhary

## Problem

Aikya needs a polished, accessible local authentication experience now and a secure path to social sign-in and stronger account protection later. Decorative OAuth buttons, browser-stored long-lived bearer tokens, or MFA without recovery would create false expectations and security risk.

## Options considered

1. Replace the current flow with a long-lived bearer token in browser storage.
2. Use a server session/refresh credential in an HttpOnly cookie and keep the short-lived access token only in memory.
3. Add provider buttons before OAuth applications, callback URLs, account linking, and threat-model verification exist.
4. Keep local authentication complete now, then add real provider adapters and MFA as reviewed vertical slices.

## Decision

- Retain the implemented rotating refresh session in a `Secure`, `HttpOnly`, appropriately `SameSite`, path-scoped cookie. The short-lived access token remains memory-only.
- Local registration accepts passwords of 8–128 characters with at least three of uppercase, lowercase, number, and symbol character classes. Passwords remain Argon2id hashed.
- Auth forms provide accessible field validation, explicit placeholders, password visibility controls, bounded toast feedback, and responsive UI states.
- Google is the only displayed provider and uses a real backend flow; missing credentials fail with an explicit safe message. Microsoft, LinkedIn, Facebook, and X stay hidden until independently implemented and approved. A social button must never be decorative or silently fail.
- Google and Microsoft should use standards-based OpenID Connect Authorization Code + PKCE. LinkedIn uses its supported OIDC flow where available. Facebook and X require provider-specific OAuth adapters and normalized identity claims.
- Every provider implementation requires state, nonce where applicable, PKCE, exact redirect allowlists, verified-email/account-linking policy, generic errors, audit events, rate limits, secret rotation, and provider-specific privacy documentation.
- WebAuthn passkey MFA is implemented with user verification, one-time challenges, signature counters, first-enrollment recovery codes stored only as keyed hashes, and enforcement after both password and Google authentication. Credential revocation, lost-device support review, audit events, and abuse-resistant reset remain private-beta gates.

## Consequences

- Phase 1 exposes local authentication plus Google only; no other provider is implied.
- Existing HttpOnly session security is preserved. `PyJWT[crypto]` verifies signed OAuth state/Google ID tokens, `webauthn` verifies server ceremonies, and `@simplewebauthn/browser` serializes browser ceremonies.
- OAuth still requires a real Google developer application and uncommitted credentials for runtime use.
- MFA persistence and recovery are implemented; credential management, audit, reset, and final security validation remain release gates.

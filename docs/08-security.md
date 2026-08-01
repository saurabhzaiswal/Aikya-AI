# Security and Privacy Architecture

Status: Baseline controls; formal threat model required before implementation  
Security objective: protect tenant isolation, document confidentiality, account integrity, billing correctness, and service availability

## Data classification

| Class | Examples | Handling |
|---|---|---|
| Restricted content | source/translated files, extracted text, OCR regions, AI prompts/results | encrypted, least privilege, no logs/analytics, explicit retention |
| Sensitive identity | email, OAuth subject, session metadata, IP as retained by policy | encrypted transport/storage, access limited, retention documented |
| Secret | passwords, refresh/API tokens, provider/payment credentials, signing keys | hash where verifiable; otherwise secrets manager/envelope encryption |
| Confidential business | usage, invoices, membership, audit records | tenant-scoped and audited |
| Public | marketing pages, published format/language capability | integrity protected |

## Threat model summary

Primary threats include account takeover, cross-tenant object access, signed-URL leakage, malicious parser files, archive/decompression bombs, SSRF/XXE/path traversal, provider data exposure, queue replay/duplication, billing fraud, API abuse, supply-chain compromise, privileged support abuse, and incomplete deletion.

Threat modeling follows trust boundaries shown in the architecture/deployment diagrams and is updated for every new parser, provider, client, public API, or sharing feature.

## Identity controls

- OAuth Authorization Code + PKCE with state, nonce, issuer, audience, redirect URI, and verified-email policy.
- Local passwords use Argon2id with parameter review, breached-password defense, verification, and rate-limited generic errors.
- Short-lived access token in memory; rotating refresh token in Secure, HttpOnly, appropriately SameSite cookie, stored only as hash server-side.
- Session family replay detection revokes the family and notifies the user.
- CSRF protection on cookie-authenticated mutations; strict CORS allowlist.
- Step-up authentication and MFA before high-impact organization/admin actions; MFA becomes user-facing before enterprise launch.

## Authorization and tenancy

- Deny by default. Permission checks live in use cases and receive resolved actor + organization context.
- Every tenant query includes organization scope; every object key maps to an authorized file record.
- Fixed roles begin with owner, admin, member, and viewer. Permissions are centrally defined and matrix-tested.
- Last-owner removal, invitation acceptance, organization switch, export, delete, and billing actions are transactional.
- PostgreSQL row-level security is defense in depth before multi-user business tenancy, not a substitute for application checks.
- Support/admin has no implicit content access. Approved access is time-bound, reasoned, step-up authenticated, and audited.

## File security

1. Authorize an upload intent and constrain content length/type/checksum.
2. Upload into a private quarantine prefix with short expiry.
3. Verify object attributes and file signature independently of filename/header.
4. Scan malware and validate format structure, page count, decompression ratio, nesting, and active content.
5. Reject or neutralize macros, external relationships, embedded executables, scripts, and unsafe URLs by policy.
6. Process in isolated, non-root, read-only containers with ephemeral scratch, syscall/capability restrictions, CPU/memory/time caps, and no network unless explicitly needed.
7. Publish clean output under a new randomized key only after validation.

HTML/EPUB/SVG preview uses sanitization and a sandboxed origin. PDF/Office parsers are patched aggressively. User-supplied filenames are display metadata only and never filesystem paths.

## Object storage

- Private buckets/prefixes separate quarantine, clean source, intermediate, and output classes.
- TLS, server-side encryption, bucket public-access blocks, versioning policy, lifecycle rules, and access logs.
- Signed URLs are short-lived, method/key/content-length constrained, and never logged.
- IAM grants each runtime only required prefix/actions; workers do not have bucket administration.
- Object keys are random and tenant-independent in appearance; database authorization is mandatory.

## Provider privacy and egress

Maintain a provider register covering data location, subprocessors, retention/training terms, security, DPA, supported languages, and deletion. Each organization policy states allowed providers and privacy class. Users see when content leaves Aikya and when optional AI is invoked.

Worker network policy allows only required storage/database/queue endpoints and the selected provider. Provider credentials are scoped and rotated. Payloads, provider request bodies, and provider raw errors are not logged.

## API and browser security

- Strict validation, bounded payloads, parameterized queries, safe serialization, and content-type enforcement.
- Rate limits by IP, account, organization, key, endpoint, and job class; separate credential-stuffing controls.
- HSTS, CSP, frame restrictions, MIME sniffing protection, referrer/permissions policies, secure cookie flags.
- No secrets or long-lived tokens in local storage, source maps, client bundles, URLs, or analytics.
- Dependency pinning, vulnerability review, SAST, secret scan, container scan, SBOM, and provenance/signing where platform support permits.
- Browser extension later uses minimal optional host permissions, isolated content scripts, sanitized rendering, and no trust in page JavaScript.

## Privacy lifecycle

- Collect only data required for the chosen action.
- Allow temporary processing without indefinite storage.
- Associate each artifact with purpose, retention class, expiry, and lineage.
- Deletion jobs erase active source, intermediate, output, thumbnails, cache, search copies, and provider-side artifacts where supported; record a content-free tombstone.
- Explain backup expiry separately from active deletion.
- Export/deletion requests require current authentication, anti-replay protection, and audit.
- Never use user documents or translations to train Aikya models without a future separate, explicit, revocable program; the baseline is no training.

## Secrets and encryption

Production secrets come from a secrets manager at runtime. Development uses uncommitted local environment values derived from `.env.example`. Keys differ by environment and service. Rotation and compromise runbooks cover database, storage, OAuth, signing, payment, provider, and CI credentials.

Use TLS for external/internal connections where supported. Managed encryption at rest protects database, backups, storage, and logs. Highly sensitive tokens use application-layer envelope encryption only where hashing is impossible. Key access is audited.

## Audit and logging

Audit records capture actor, action, target ID/type, tenant, outcome, request ID, safe metadata, and timestamp. Authentication, membership, provider policy, retention, API key, billing, export/delete, and admin actions are audited.

Operational logs contain IDs and safe codes—not names, emails where avoidable, text, filenames, tokens, signed URLs, or provider payloads. Error trackers scrub headers, body, query strings, breadcrumbs, and attachments.

## Security verification

- Tenant authorization matrix and object-key access tests.
- Malicious/corrupt document corpus and parser sandbox escape review.
- Authentication rotation/replay, OAuth, CSRF, CORS, and session revocation tests.
- Rate-limit, quota, duplicate-job, and billing webhook abuse tests.
- Dependency/container/IaC scanning and external penetration test before public/enterprise launch.
- Backup restore, key rotation, incident response, and deletion drills.

## Incident response

Maintain severity definitions, on-call contacts, evidence preservation, containment, customer/regulator communication decision paths, credential rotation, provider suspension, and post-incident review. Runbooks must cover account compromise, suspected cross-tenant access, exposed signed URL/key, malicious file, provider leak/outage, billing webhook fraud, and deletion backlog.

## Phase 1 implementation status — 2026-08-01

Implemented controls include Argon2id password hashing, short-lived signed access tokens, hashed rotating HttpOnly refresh sessions with replay-family revocation, tenant checks on user resources, Redis-backed abuse limits, private randomized object keys, short-lived signed upload/download URLs, PDF signature/size/checksum/page/password checks, fail-closed clamd scanning before parsing, content-safe public errors, and no browser persistence for bearer tokens.

This is not a completed security review or compliance claim. Docker-integrated scanner/storage/provider validation, automated tenant and session abuse coverage, active deletion/retention automation, dependency/image scanning, parser sandbox/resource enforcement, restore/deletion drills, and final threat-model verification remain required before private beta.

## Compliance position

Architecture supports future GDPR, SOC 2, ISO 27001, and sector-specific work, but no compliance claim is valid without applicable legal analysis, policies, evidence, vendor agreements, training, audits, and continuous operation.

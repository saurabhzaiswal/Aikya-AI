# Aikya AI Privacy Policy — Draft

Status: Internal product draft; not yet effective  
Owner: Saurabh Choudhary  
Last updated: 2026-08-01

This draft describes the intended Phase 1 data practices so product behavior and future legal review stay aligned. It must not be published as an effective policy until deployment providers, operating entity/contact details, launch regions, retention periods, user-rights process, and legal basis are confirmed by the founder and qualified counsel.

## Phase 1 data categories

- Account data: email address, display name, password hash, session records, locale, and personal workspace identifiers.
- User content: text submitted for translation, source digital PDFs, translated text, and generated readable PDFs.
- Operational metadata: timestamps, job state, language choices, file size/checksum, safe request IDs, rate-limit keys, and content-free service logs.

Passwords and raw refresh tokens are not stored. Document text, credentials, signed URLs, and provider payloads must not appear in logs or analytics.

## Processing and service providers

Aikya processes data to authenticate users, provide translations, process digital PDFs, protect the service, and diagnose content-free operational failures. Translation content is sent only to the server-configured translation provider. The production provider, processing region, subprocessors, retention/training terms, and user disclosure remain launch decisions.

## Storage, retention, and deletion

Phase 1 uses private object storage and tenant-scoped database records. Temporary artifacts currently carry expiry metadata. Active deletion/retention automation and the user deletion workflow are not yet release-ready and remain mandatory private-beta gates. No public deletion-time promise should be made until those controls and backup expiry are verified.

## User rights and contact

Access, correction, export, objection, and deletion procedures depend on launch jurisdiction and operating details. Effective contact information and response timelines must be added before publication.

## Security

Current controls include encrypted transport at deployment, password hashing, rotating sessions, private signed object access, tenant authorization, upload validation, malware scanning, rate limiting, and content-safe errors. No system can promise absolute security, and this draft makes no compliance certification claim.

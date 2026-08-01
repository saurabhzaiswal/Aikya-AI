# ADR-015: Phase 1 Runtime, Identifier, Localization, and CI Baselines

Date: 2026-08-01  
Status: Accepted by founder instruction

## Problem

The Nuxt migration still targeted an older Node baseline, the backend excluded Python 3.14, ORM entities generated UUIDv4 primary keys, localization had only a design requirement, and no remote CI workflow enforced master-branch quality. These inconsistencies make local operation and regressions harder for a solo founder.

## Options considered

1. Keep Node 22/Python 3.12, UUIDv4, untranslated UI, and manual checks.
2. Adopt Node 24.18.x and Python 3.14+, native Python UUIDv7 entity IDs, official Nuxt i18n with English fallback, and GitHub Actions CI.
3. Add multiple compatibility runtimes, database-generated identifiers, a custom localization layer, and both GitHub/GitLab pipelines.

## Decision

Use Node.js `>=24.18.0 <25` and Python `>=3.14`. Generate persisted entity/business identifiers through the shared Python 3.14 `uuid7()` wrapper. Keep UUIDv4 only for non-persisted security-random request/JWT correlation values.

Use official Nuxt i18n with lazy English and Hindi catalogs, `prefix_except_default` public routing, locale SEO metadata, and English as the complete fallback locale. Private application/auth routes remain unprefixed to preserve existing security/routing boundaries.

Use GitHub as the recommended remote and `.github/workflows/ci.yml` for push/pull-request validation on `master`. CI performs lint, typing, production builds, migration-graph validation, UUID regression detection, Compose validation, and container builds. Deployment remains manual; no CD credentials or jobs are introduced.

Frontend lifecycle ownership and leak profiling follow `docs/frontend-memory-safety.md`; unexplained memory growth is a release blocker.

## Reasons

- These versions match the founder's current machine and make native Python UUIDv7 available without another identifier dependency.
- UUIDv7 improves index locality while retaining globally unique opaque IDs.
- Official Nuxt i18n integrates routing, fallback, lazy catalogs, and language SEO without a custom framework.
- One GitHub workflow is lower maintenance and fits the founder's existing public GitHub identity.
- Explicit lifecycle rules are more enforceable than an unverifiable promise that leaks can never occur.

## Consequences

- Older Node/Python runtimes fail package installation by design.
- Existing local UUIDv4 rows remain valid UUID values, but every newly generated persisted ID is UUIDv7; there is no production data migration at this pre-beta stage.
- English/Hindi application chrome is localized now; remaining Phase 1 feature copy moves to message keys incrementally before beta.
- GitHub branch protection must be enabled in repository settings to require CI before merge.
- CI has no deployment authority and production remains gated by the documented acceptance work.

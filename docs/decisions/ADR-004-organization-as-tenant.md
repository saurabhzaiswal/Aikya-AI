# ADR-004: Use Organizations as the Tenant Boundary

Date: 2026-08-01  
Status: Accepted for Phase 1  
Decision authority: Founder-approved Phase 1 scope

## Context

Aikya needs explicit tenant isolation from the first user while Phase 1 exposes only personal accounts. Adding tenant ownership later would require risky data and authorization migrations.

## Options considered

1. Organization tenancy with a personal organization/workspace for every user.
2. User-owned resources now and organizations added later.
3. Team-only organizations with a separate personal-resource model.

## Decision

Every business resource is organization-scoped. Registration transactionally creates the user, owner membership, personal organization, and default workspace. API authorization resolves and validates active membership server-side.

## Reason

One ownership model prevents a later tenancy retrofit and supports personal users now without implementing Phase 1 team-management features.

## Consequences

- All tenant-owned queries and object prefixes require `organization_id`.
- Personal tenancy does not imply team, invitation, or role-management UI in Phase 1.
- Automated cross-tenant tests are mandatory before private beta.
- Future organization switching requires a separate product/security decision.

# User and Dashboard API Contract - Phase 1

Base path: `/api/v1`

## `GET /auth/me`

Returns authenticated user ID, email, display name, locale, active organization, and workspace. Sensitive auth/session fields are excluded.

## Profile update (planned before beta)

The first Phase 1 cut is read-only. A later `PATCH /users/me` may permit display-name and locale updates only. Email/password changes remain separate security workflows.

## `GET /dashboard/summary`

Returns tenant-scoped counts for documents by public state, recent documents, recent text translations, and current supported limits. No document content appears in aggregate telemetry.

## Authorization

All operations resolve the authenticated user's active personal organization server-side. Phase 1 does not expose team, invitation, role-management, billing, or admin endpoints.

# Authentication API Contract — Phase 1

Base path: `/api/v1/auth`  
Authentication: short-lived bearer access token plus rotating HttpOnly refresh cookie

## Operations

### `POST /register`

Accepts email, password, display name, and an optional BCP 47 locale (default `en`). Creates a user plus personal organization/workspace transactionally. Returns public user, organization/workspace context, and access token; sets refresh cookie. Duplicate email returns a generic conflict without disclosing unnecessary state.

### `POST /login`

Accepts email/password. On success rotates/creates a session, returns access token and public context, and sets refresh cookie. Invalid credentials return `401 invalid_credentials`. Apply IP/email-keyed abuse limits.

### `POST /refresh`

Consumes current refresh cookie, verifies stored hash/family/expiry/revocation, rotates it, and returns a new access token plus cookie. Replay revokes the family.

### `POST /logout`

Revokes the current refresh session, clears cookie, and returns `204`. The operation is idempotent.

### `GET /me`

Requires access token. Returns user, active personal organization, and workspace summary.

### `PATCH /me/locale`

Requires access token. Accepts `{ "locale": "hi" }`, persists the validated locale preference on the current user, and returns the updated public user. It stores no IP address or inferred location.

## Security contract

Passwords are never returned/logged and use Argon2id. Refresh cookie is HttpOnly, SameSite=Lax, Secure in production, path-scoped, and has bounded age. Access tokens are held in browser memory. Auth errors follow the common content-safe envelope.

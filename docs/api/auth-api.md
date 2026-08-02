# Authentication API Contract - Phase 1

Base path: `/api/v1/auth`  
Authentication: short-lived bearer access token plus rotating HttpOnly refresh cookie

## Operations

### `POST /register`

Accepts email, an 8–128 character password using at least three character classes, display name, and an optional BCP 47 locale (default `en`). Creates a user plus personal organization/workspace transactionally. Returns public user, organization/workspace context, and access token; sets refresh cookie. Duplicate email returns a generic conflict without disclosing unnecessary state.

### `POST /login`

Accepts email/password. Without MFA it creates a session, returns access token and public context, and sets the refresh cookie. When passkey 2FA is enabled it returns `status: mfa_required`, a one-time challenge ID, and WebAuthn request options without issuing a session. Invalid credentials return `401 invalid_credentials`. Apply IP/email-keyed abuse limits.

### `GET /oauth/google/start`

Starts the real Google OpenID Connect Authorization Code flow with state, nonce, and PKCE. `return_to` accepts only an internal dashboard path. Provider credentials come only from the runtime environment.

### `GET /oauth/google/callback`

Validates the signed state cookie, exchanges the code server-to-server, verifies the Google ID token and verified email, safely resolves or links the local account, and sets the normal rotating refresh cookie before redirecting to the internal dashboard. Accounts with Aikya MFA enabled must complete WebAuthn before a session is issued.

### WebAuthn operations

- `GET /webauthn/status` lists the current user's registered passkeys.
- `POST /webauthn/register/options` creates a short-lived one-time enrollment challenge.
- `POST /webauthn/register/verify` verifies attestation, stores the credential public key/counter, enables MFA, and returns plaintext recovery codes only on first enrollment.
- `GET /webauthn/oauth/options` resumes the second-factor challenge after Google callback using a short-lived HttpOnly ticket.
- `POST /webauthn/authenticate/verify` verifies assertion, consumes the challenge, updates the signature counter, and only then issues the session.
- `POST /webauthn/recovery/verify` consumes one keyed-hash recovery code and issues the session.

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

OAuth state and WebAuthn challenges are short lived and one-time. Persisted identity, credential, challenge, and recovery-code records use application-generated UUIDv7 IDs. Google client secrets, authenticator private keys, plaintext recovery codes, and long-lived tokens never enter the frontend bundle or committed files.

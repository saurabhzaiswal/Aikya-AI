# Contributing to Aikya AI

Read `AGENTS.md`, `docs/PROJECT_STATUS.md`, `docs/project-progress.md`, relevant specifications, and accepted ADRs before changing the repository.

## Branches

- `feature/short-description`
- `fix/short-description`
- `docs/short-description`
- `refactor/short-description`
- `security/short-description`
- `chore/short-description`

Keep branches focused on one approved outcome.

## Commits

Use imperative Conventional Commit prefixes:

- `feat:` user-visible capability
- `fix:` defect correction
- `docs:` documentation only
- `refactor:` behavior-preserving code change
- `security:` security/privacy hardening
- `chore:` tooling or maintenance

Do not include secrets, generated noise, customer data, or unrelated changes.

## Pull requests

Describe the problem, linked requirements/ADR, scope, files/modules, data/API/UX impact, security/privacy implications, verification evidence, deployment/migration behavior, rollback, and documentation updates. Major architecture/stack/provider/retention/public-contract decisions require founder approval.

## Documentation synchronization

Update relevant docs before a major feature and again after implementation. Update project status/progress, sprint notes, and changelog only with verified outcomes. Supersede ADRs rather than deleting decision history.

## Quality

Follow Vue Options API, FastAPI modular boundaries, tenant scoping, provider adapters, Docker-only runtime dependencies, accessibility, and secret/content-safe logging. Automated suites are temporarily deferred for the current phase, but static/build/migration/smoke verification remains mandatory.

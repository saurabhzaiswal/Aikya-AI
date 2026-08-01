# Backup and Recovery Strategy

## Scope

Protect PostgreSQL transactional state, private object metadata/content according to retention promises, configuration/IaC, and release artifacts. Redis is transient and must be reconstructable.

## Proposed beta objectives

- Recovery point objective: up to 24 hours.
- Recovery time objective: up to 4 hours.

These are targets until demonstrated by restore drills and are tightened before contractual enterprise commitments.

## PostgreSQL

Use encrypted automated backups, provider-managed point-in-time recovery where available, separate backup credentials, retention monitoring, and periodic restoration into an isolated environment. Validate schema version, tenant integrity, jobs, usage, and file references after restore.

## Object storage

Use encryption, version/lifecycle policy, integrity metadata, and optional cross-region replication only when it does not violate residency/deletion rules. Source, intermediate, and output retention must match the user's selected policy.

## Redis and queues

Redis failure may delay jobs but cannot erase accepted work. Recover durable job state from PostgreSQL, re-dispatch safe stages, and rely on idempotency to prevent duplicate output/usage.

## Deletion interaction

Customer deletion removes active copies promptly and ages out encrypted backups on the disclosed schedule. Restoration procedures must reapply deletion tombstones so erased content is not silently resurrected.

## Drills

Before beta, test database restore, object referential integrity, worker/job recovery, credential rotation, and deletion replay. Record duration, data loss window, failures, owners, and corrective actions.

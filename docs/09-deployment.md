# Deployment and Environment Architecture

Status: Foundation design  
Source diagram: [`diagrams/deployment.excalidraw`](diagrams/deployment.excalidraw)

## Environment model

| Environment | Purpose | Data policy |
|---|---|---|
| Local | developer iteration through Docker Compose | synthetic/local only |
| CI | isolated automated validation | ephemeral synthetic fixtures |
| Staging | production-like release validation | synthetic or approved test data; never copied production content |
| Production | customer workloads | controlled restricted data |

Accounts/projects, network, database, buckets, secrets, OAuth apps, payment modes, and provider keys are separate. Builds are promoted between environments; code is not rebuilt for production.

## Container topology

Production containers include edge/Nginx, the Nuxt Nitro SSR frontend, FastAPI API, document/translation/render workers, and supporting data services. OCR, a scheduler, and an outbox dispatcher remain future topology until an approved feature requires them. PostgreSQL, Redis, object storage, secrets, and telemetry should be managed services where the selected platform supports the required controls. Compose production definitions provide a single-server/reference topology, not the final million-user orchestration platform.

All application images:

- use pinned base versions and reproducible dependency locks;
- run as non-root with read-only filesystem and explicit writable temporary mount;
- contain health/readiness behavior;
- handle termination and drain workers;
- expose no development server/debugger;
- receive secrets at runtime;
- carry version/commit metadata and produce an SBOM.

Application builds use dedicated `frontend/` and `backend/` contexts with local `.dockerignore` policies; repository root is never a normal build context. The worker and migration roles reuse the same immutable backend image. Layer/context details and measured reductions are maintained in [`docker-optimization.md`](docker-optimization.md).

## Local Docker workflow

From the repository root, `docker compose up` loads the Phase 1 development stack. It builds the Nuxt frontend and shared FastAPI/Celery backend image, runs migrations before application startup, creates private MinIO buckets, waits for PostgreSQL/Redis/storage health, and requires ClamAV to become healthy before workers accept PDF jobs.

The stack includes frontend, backend, worker, PostgreSQL, Redis, MinIO, and a bucket-initialization job. Persistent data uses named volumes; `docker compose down` is non-destructive unless the operator explicitly adds `--volumes`.

## Production Compose policy

`docker/docker-compose.prod.yml` requires immutable application image references supplied by deployment configuration. It defines health checks, restart policy, dependency health, read-only/runtime limits where portable, internal networks, persistent state, and no source mounts. It is a reference deployment for pilot/single-host use.

Production databases and object storage should move to managed services before meaningful customer scale. Compose is not high availability: one host is a failure domain and does not provide multi-zone scheduling, autoscaling, managed secret rotation, or zero-downtime database failover.

## Edge and Nginx

Nginx routes `/api/` to the backend and other paths to the Nuxt Nitro frontend, applies safe headers, bounded request rules, timeouts, and correlation forwarding. Binary uploads bypass Nginx through signed object requests. TLS termination may live at a cloud load balancer; exactly one layer owns redirect/HSTS behavior to avoid loops.

## CI/CD pipeline

The first repository CI implementation lives at `.github/workflows/ci.yml` and runs on pushes and pull requests to `master`. It uses Node.js 24.18.0 and Python 3.14, validates locked dependencies, lint/types/builds, migration heads, the UUIDv7 model policy, development Compose, and production container builds. Docker Buildx persists independent GitHub cache scopes for the frontend and backend contexts. CI has read-only repository permissions and no deployment credentials. CD remains intentionally unimplemented.

1. Lint, formatting, type checking, secret detection, and architecture-boundary validation.
2. Unit, integration, contract, security, and bounded golden-document tests.
3. Migration upgrade tests from clean and supported previous schema.
4. Build immutable frontend/backend images once.
5. Scan dependencies/images, generate SBOM, and sign/attest when available.
6. Deploy by digest to staging, run smoke/accessibility/security/pipeline checks.
7. Require approval and promote identical digests to production.
8. Observe release SLOs and roll back application version if thresholds burn.

Database changes follow expand/migrate/contract. Rollback never assumes destructive down-migration. Feature flags separate deployment from exposure.

## Health and lifecycle

- Liveness: process/runtime is responsive; it must not depend on every external provider.
- Readiness: instance can safely receive work, including required database/config checks.
- Startup: migration/bootstrap delays do not trigger false liveness failure.
- Worker health: heartbeat and queue connectivity plus PostgreSQL job recovery; no HTTP-only illusion.
- Dependency ordering in Compose is convenience; applications still retry connections safely.

## Configuration and secrets

Configuration is validated at startup and grouped by database, Redis/queue, storage, auth, provider, billing, limits, retention, and telemetry. `.env.example` documents keys with safe/non-secret placeholders. Production secrets are never stored in Compose YAML, shell history, build arguments, logs, or GitHub Actions output.

## Backup and recovery

- Automated encrypted PostgreSQL backups with point-in-time recovery when the provider supports it.
- Object storage version/lifecycle policy aligned to deletion promises.
- Redis is reconstructable/transient; job truth recovers from PostgreSQL.
- Restore drills verify application compatibility and document/object referential integrity.
- Beta proposal: RPO 24 hours, RTO 4 hours; tighten before contractual SLOs.

## Observability and operations

Collect structured logs, OpenTelemetry traces, Prometheus-compatible metrics, and error events with content scrubbing. Dashboards cover API, database, Redis, queue, workers, providers, storage, job outcomes, costs, quality, billing reconciliation, and deletion backlog.

Alerts are routed by user impact/SLO burn. Runbooks cover high queue age, provider outage/rate limit, database saturation, storage failure, stuck jobs, failed deletion, billing webhook backlog, bad deployment, and credential compromise.

## Production readiness gate

- Cloud/region, managed data services, secret manager, DNS/TLS, email/OAuth/payment providers approved.
- Capacity/load and provider-failure tests pass.
- Backups restore and deletion lifecycle is demonstrated.
- No mutable/unpinned application tags.
- Network and IAM least privilege reviewed.
- Dashboards, alerts, on-call, incident contacts, and rollback tested.
- Privacy/security/customer claims match operational evidence.

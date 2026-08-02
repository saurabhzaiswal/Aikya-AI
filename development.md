# Aikya AI Development Environment

Status: Phase 1 Nuxt migration implemented; frontend build and container runtime acceptance pending

## Required host tools

- Docker Desktop or Docker Engine with Docker Compose v2.
- Git.
- Optional editor with Markdown, YAML, and Excalidraw support.

Python, Node.js, PostgreSQL, Redis, MinIO, and ClamAV are not required on the host; their toolchains and services run inside containers.

When running application checks natively, use Node.js 24.18.x and Python 3.14+. The canonical operator commands are maintained in [RUNBOOK.md](RUNBOOK.md).

## First-time setup

From the repository root:

```powershell
Copy-Item .env.example .env
docker compose up -d
docker compose ps
```

Open the frontend on `http://localhost:3000`, API docs on `http://localhost:8000/api/docs`, backend readiness on `http://localhost:8000/health/ready`, and MinIO console on `http://localhost:9001` using the development-only credentials from `.env`.

The frontend, backend, and worker build the Phase 1 Nuxt/FastAPI application. PostgreSQL migrations run through the one-shot `migrate` service before the API and worker become healthy.

## Compose files

- `compose.yaml`: root entry so `docker compose up` works as requested.
- `docker/docker-compose.yml`: runnable foundation development stack.
- `docker/docker-compose.dev.yml`: optional developer overrides such as direct database/cache ports.
- `docker/docker-compose.prod.yml`: secure reference production topology requiring real application image references.

Every application build is context-scoped: Nuxt uses `frontend/`; API, worker, and migrate use the shared `backend/` application image from `backend/`. Root context builds are prohibited. See the measured [Docker optimization report](docs/docker-optimization.md).

Start with extra development ports:

```powershell
docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up -d
```

Validate Compose without starting services:

```powershell
docker compose -f docker/docker-compose.yml config --quiet
docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml config --quiet
```

## Common commands

```powershell
docker compose ps
docker compose logs -f backend worker
docker compose restart backend
docker compose stop
docker compose down
```

`docker compose down` retains named volumes. Adding `--volumes` permanently removes local database/storage/cache data and must be intentional.

## Services and ports

| Service | Container port | Default host port | Purpose in foundation phase |
|---|---:|---:|---|
| frontend | 3000 | 5173 | Nuxt 4 development application |
| backend | 8000 | 8000 | FastAPI application |
| worker | none | none | Celery PDF processing worker |
| postgres | 5432 | only in dev override | real development database |
| redis | 6379 | only in dev override | real cache/queue dependency |
| minio | 9000/9001 | 9000/9001 | S3-compatible development storage/console |
| minio-init | none | none | idempotent private bucket bootstrap |
| clamav | 3310 | not exposed | isolated malware scanner used before PDF parsing |

Change host ports in `.env` when they conflict.

## Environment variables

Copy `.env.example` to the ignored `.env` file. Set `LIBRETRANSLATE_URL` (and its API key when required) to a trusted compatible provider before translating. Values are grouped by app, database, Redis, storage, authentication, provider integrations, limits, and telemetry.

Rules:

- Never commit `.env`, production credentials, provider keys, or secret files.
- Development defaults are intentionally recognizable and must not be reused elsewhere.
- Production values come from the deployment platform's secrets manager.
- Adding a setting requires validation, documentation in `.env.example`, and a safe default or startup failure.

## Production reference validation

The production file intentionally requires immutable frontend/backend image references and production secrets. Supply them in an approved deployment environment, then validate:

```powershell
docker compose --env-file .env.production -f docker/docker-compose.prod.yml config --quiet
```

Do not launch production with `.env.example`. The Compose topology is suitable for a controlled single-host pilot, not high availability. Managed PostgreSQL, Redis, object storage, secrets, load balancing, and multi-zone orchestration supersede local containers as scale and SLOs require.

## Application image contract

- `frontend` is a multi-stage Nuxt build served by a non-root Nitro/Node runtime on port 3000 in production.
- `backend` is the FastAPI ASGI image with `/health/live` and database-backed `/health/ready`.
- `worker` uses the same non-root backend image with a Celery entrypoint.
- Production roles use read-only filesystems and ephemeral scratch in the reference topology.
- Lockfiles are committed; immutable image references and supply-chain gates remain deployment requirements.

No business logic should be embedded in Compose commands.

## Engineering workflow

Before a feature begins, link its requirement IDs, ADRs, data/API/UX changes, security/privacy impact, test strategy, telemetry, migration, rollout, and rollback. Use small vertical slices. Do not bypass module boundaries or introduce a provider SDK into domain/client code.

Definition of Done is maintained in the [technical blueprint](docs/01-technical-blueprint.md) and [testing strategy](docs/10-testing.md).

## Troubleshooting

- Port conflict: change the relevant `*_PORT` value in `.env`.
- Unhealthy PostgreSQL/Redis/MinIO/ClamAV: inspect `docker compose logs <service>` and verify development credentials/resources. ClamAV signature initialization can make its first startup slower and requires substantial memory.
- Bucket init failure: ensure MinIO is healthy, then run `docker compose up minio-init` again; it is idempotent.
- Configuration issue: run the Compose `config --quiet` commands before pulling or starting containers.
- Do not delete volumes as a first troubleshooting step; preserve local data unless reset is explicitly intended.

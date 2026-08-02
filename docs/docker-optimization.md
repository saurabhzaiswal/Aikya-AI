# Docker Build Optimization

Last updated: 2026-08-01  
Status: Implemented; full-stack runtime acceptance remains pending

## Problem and audit evidence

Docker was being asked to consider local dependency trees and caches that are not application source. The repository audit measured:

| Location | Measured size | Primary causes |
|---|---:|---|
| `frontend/` | 1,161.56 MB | `.npm-cache` 754.14 MB, `node_modules` 395.38 MB, `.output` 10.38 MB, `.nuxt` 0.79 MB |
| `backend/` | 265.97 MB | `.venv314` 200.19 MB, `.mypy_cache` 34.11 MB, `.venv` 31.13 MB |
| `.uv-cache/` | 213.89 MB | downloaded/extracted Python packages and wheels |
| `.uv-python/` | 61.09 MB | locally managed Python runtime |

The frontend and backend source/configuration needed by Docker is under one megabyte per application. Local caches, generated output, virtual environments, Git/private context, documentation, logs, and environment files must never enter a build context or image.

No cache or virtual environment was deleted by this change; these are ignored, regenerable local artifacts owned by the developer.

## Context design

The root `compose.yaml` is orchestration only and includes `docker/docker-compose.yml`. It never builds from `.`.

| Role | Build context | Dockerfile | Image strategy |
|---|---|---|---|
| Nuxt frontend | `frontend/` | `frontend/Dockerfile` | dedicated frontend image |
| FastAPI backend | `backend/` | `backend/Dockerfile` | shared backend application image |
| Celery worker | `backend/` | `backend/Dockerfile` | same backend image, worker command |
| Alembic migrate | `backend/` | `backend/Dockerfile` | same backend image, migration command |

Worker and migrate are runtime roles of the FastAPI modular monolith, not independent applications. Creating duplicate source directories and Dockerfiles would duplicate dependency layers, create version drift, and weaken cache reuse. Compose gives each role only the `backend/` context and reuses the same tagged development image/build definition.

The repository root now has a defensive `.dockerignore` so an accidental `docker build .` remains bounded, but root context is prohibited for normal builds.

## Measured context improvement

The post-change context manifest contains:

| Context | Included files | Approximate payload | Reduction from directory size |
|---|---:|---:|---:|
| Frontend | 101 | 0.811 MB | 99.93% |
| Backend | 44 | 0.248 MB | 99.91% |
| Accidental root | 163 | 1.098 MB | over 99.8% versus the reported 900 MB+ transfer |

Docker BuildKit remains the final source of truth for the transferred-byte value printed during a real build. The manifest measurement applies the committed ignore policy without deleting local files.

## Verified build results

Validated on Docker Desktop/BuildKit on 2026-08-01:

| Check | Result |
|---|---|
| Frontend production image build | Pass; clean build transferred 857.10 kB |
| Backend production image build | Pass; application context is approximately 0.248 MB (an incremental BuildKit run transferred 2.29 kB) |
| Frontend runtime smoke | Pass; `/healthz` returned HTTP 200 |
| Backend runtime smoke | Pass; `app.main` imported from the production image |
| Frontend image size | 61,614,058 bytes (approximately 58.8 MiB) |
| Backend image size | 122,181,937 bytes (approximately 116.5 MiB) |
| Dockerfile BuildKit checks | Pass with no warnings |
| Development/production Compose interpolation | Pass |

An initial Docker Hub anonymous-token request for `clamav/clamav:1.4_base` encountered a TLS handshake timeout. Retrying the pinned image separately succeeded with digest `sha256:35ec19c1e8cbee7cae8a35c3b0ac62957d99b418e6902035b89a1778c39433e7`, confirming a transient registry/network failure rather than a Dockerfile issue.

During full-stack acceptance, PostgreSQL, Redis, MinIO, migrations, backend health, and frontend startup succeeded. The audit also exposed that ClamAV and the worker were attached only to an `internal: true` network, which prevented signature updates and provider calls. A dedicated, non-published egress network now fixes that architecture without exposing host ports or placing stateful data services on it. The final ClamAV health wait was interrupted when Docker Desktop's container-inspect API returned HTTP 500 and the local engine stopped responding; repeat the runtime check after Docker Desktop recovers.

## Ignore policy

- Root `.dockerignore`: Git/agent/editor context, docs, temporary data, environment/secrets, npm/uv caches, generated frontend output, virtual environments, Python caches, logs, and coverage.
- `frontend/.dockerignore`: `node_modules`, `.npm-cache`, `.nuxt`, `.output`, `.data`, caches, coverage, local environment files, and logs.
- `backend/.dockerignore`: every `.venv*`, bytecode, mypy/Ruff/pytest/uv caches, build artifacts, tests, local environment files, and logs.

Required lockfiles, application source, Nuxt configuration/content/public assets, Alembic migrations, and `alembic.ini` remain available to their builds.

## Layer and image strategy

### Frontend

1. Copy `package.json` and `package-lock.json` first.
2. Run `npm ci` with a BuildKit npm cache mount.
3. Copy the filtered application source only after the dependency layer.
4. Build Nuxt in a builder stage with the public site URL as a non-secret build argument so prerendered canonical URLs are not localhost.
5. Copy only `.output` into the non-root Node production stage.

### Backend

1. Start from the Python 3.14 slim runtime contract.
2. Copy `pyproject.toml` and `uv.lock` before source.
3. Resolve locked dependencies with a BuildKit uv cache mount and without installing the local project.
4. Use a development stage with dev tools and source.
5. Copy only the production virtual environment, application, and migrations into a clean non-root runtime stage; the uv binary/cache and dev tools do not enter production.

No build secret is accepted through `ARG` or copied from `.env`.

## Development and CI caching

Development retains the frontend source mount plus a named `node_modules` volume, and narrow backend source/migration mounts. PostgreSQL, Redis, MinIO, and ClamAV data remain named volumes.

PostgreSQL, Redis, and MinIO stay only on an internal network. ClamAV joins both the internal network and a dedicated non-published egress network so it can retrieve signed malware definitions. The worker also joins egress for translation-provider calls; the production backend joins it for synchronous provider operations. Egress membership does not publish a host port.

Dockerfiles use BuildKit cache mounts for npm and uv downloads. GitHub CI uses Docker Buildx with separate GitHub cache scopes for frontend and backend so one image cannot overwrite the other's cache. The CI path contexts are explicitly `frontend` and `backend`.

## Validation commands

```powershell
docker compose --env-file .env.example config --quiet
docker compose --env-file .env.example -f docker/docker-compose.yml -f docker/docker-compose.dev.yml config --quiet
docker buildx build --check frontend
docker buildx build --check backend
docker build --target production --build-arg NUXT_PUBLIC_SITE_URL=https://your-real-domain.example --tag aikya-frontend:context-check frontend
docker build --target production --tag aikya-backend:context-check backend
```

Production Compose intentionally requires real values. Validate it with the deployment environment's secret injection; never weaken required-variable checks or place secrets in build arguments.

## Maintenance rules

1. Never set an application build context to repository root.
2. Update the relevant `.dockerignore` when a tool introduces a generated/cache directory.
3. Copy lock/manifest files before source and keep dependency installation in its own layer.
4. Do not copy `.env`, credentials, local package caches, virtual environments, tests, documentation, or generated output into production images.
5. Backend, worker, and migrate must use one immutable backend image digest for a release.
6. Run BuildKit Dockerfile checks, Compose validation, and both production image builds in CI.
7. Inspect context transfer and image history after dependency/toolchain changes; unexpected multi-megabyte source-layer growth blocks merge.
8. Do not delete local volumes/caches as an automatic optimization step. Cleanup is an explicit developer operation and must not affect source or persisted application data.
9. Keep ClamAV, the worker, and production backend attached to the dedicated egress network; do not attach PostgreSQL, Redis, or MinIO to it.

# Aikya AI Runbook

This is the canonical operator guide for running Aikya AI locally and using the current single-host production reference. Run commands from the repository root unless a section says otherwise.

## Supported toolchain

- Recommended local path: Docker Desktop/Engine with Docker Compose v2 and Git.
- Native application toolchain: Node.js `24.18.0` (supported range `>=24.18.0 <25`) and Python `3.14` (the current founder machine uses Python `3.14.6`).
- Dependency managers: npm with the committed lockfile and uv with the committed lockfile.

Docker is the default because it also supplies PostgreSQL, Redis, MinIO, ClamAV, the Celery worker, and migrations consistently.

Docker builds are intentionally scoped to `frontend/` and `backend/`; never run `docker build .`. Worker and migrate reuse the backend image with different commands. See [`docs/docker-optimization.md`](docs/docker-optimization.md) for the context audit and cache policy.

## Run locally on a laptop

### 1. Create local configuration

PowerShell:

```powershell
Copy-Item .env.example .env
```

Bash:

```bash
cp .env.example .env
```

Edit only the ignored `.env`. Configure `LIBRETRANSLATE_URL` and its key when the selected trusted provider requires one. Development placeholder secrets must never be reused in production.

### 2. Start the complete development stack

```powershell
docker compose up --build -d
docker compose ps
```

First startup can be slower while ClamAV initializes signatures and application images build.

### 3. Open and verify

| Surface | URL |
|---|---|
| Nuxt application | `http://localhost:3000` |
| FastAPI documentation | `http://localhost:8000/api/docs` |
| Backend readiness | `http://localhost:8000/health/ready` |
| MinIO console | `http://localhost:9001` |

```powershell
docker compose logs -f frontend backend worker
```

Register a synthetic local account, translate short non-sensitive text, then upload a synthetic text-based PDF. A scanned PDF needs future OCR and is intentionally rejected in Phase 1.

### Registry, ClamAV, and Docker Desktop recovery

If Docker Hub reports an anonymous-token `TLS handshake timeout`, keep TLS verification enabled and retry the pinned pull separately:

```powershell
docker pull clamav/clamav:1.4_base
docker compose pull --ignore-buildable
docker compose up -d
```

ClamAV downloads its malware definitions on first start through the dedicated egress network and stores them in the named `clamav-data` volume. Follow initialization with:

```powershell
docker compose logs -f clamav
docker compose ps
```

If Docker Desktop returns HTTP 500 for its Linux-engine API or even `docker ps` stops responding, restart Docker Desktop from its UI, wait for the engine to report ready, and run `docker compose up -d` again. Do not disable TLS, use `docker system prune`, or remove named volumes as a connectivity workaround.

### 4. Stop safely

```powershell
docker compose stop
docker compose down
```

`docker compose down` retains named data volumes. Do not add `--volumes` unless permanent deletion of local PostgreSQL, Redis, and MinIO data is intentional.

## Run application checks natively

These checks use the founder's installed Node/Python versions but do not replace the Docker integration flow.

```powershell
Set-Location frontend
npm ci
npm run lint
npm run typecheck
npm run build
Set-Location ..\backend
uv sync --frozen
uv run ruff check .
uv run mypy app
uv run alembic heads
Set-Location ..
```

## Current production reference

The repository has CI but intentionally has no automatic deployment. `docker/docker-compose.prod.yml` is a controlled single-host pilot topology, not a high-availability production platform. Before real customer traffic, approve DNS/TLS, backups, managed secrets, provider privacy, monitoring, deletion/retention, restore testing, and the remaining security gates.

### 1. Build or obtain immutable application images

For a local production rehearsal:

```powershell
docker build --target production --build-arg NUXT_PUBLIC_SITE_URL=https://your-real-domain.example -t aikya-frontend:0.1.0 frontend
docker build --target production -t aikya-backend:0.1.0 backend
```

For a remote host, CI or an approved release process should push versioned images to a private registry. Production should ultimately reference image digests rather than mutable `latest` tags.

### 2. Create production configuration

```powershell
Copy-Item .env.production.example .env.production
```

Set at minimum the required database, Redis, storage, authentication, origin, translation-provider, and image variables. For a local rehearsal:

```text
AIKYA_FRONTEND_IMAGE=aikya-frontend:0.1.0
AIKYA_BACKEND_IMAGE=aikya-backend:0.1.0
```

Keep `.env.production` outside Git and supply real secrets through the deployment platform's secret store.

### 3. Validate and start

```powershell
docker compose --env-file .env.production -f docker/docker-compose.prod.yml config --quiet
docker compose --env-file .env.production -f docker/docker-compose.prod.yml up -d
docker compose --env-file .env.production -f docker/docker-compose.prod.yml ps
```

The one-shot `migrate` service runs `alembic upgrade head` before the backend and worker. Do not run destructive downgrade migrations during rollback.

### 4. Verify and operate

```powershell
docker compose --env-file .env.production -f docker/docker-compose.prod.yml logs -f nginx frontend backend worker migrate
```

Verify the public health endpoint, login/session rotation, tenant isolation, translation provider, private object storage, malware scanner, PDF job completion, and backup visibility. TLS must terminate at an approved load balancer/proxy before internet exposure.

### 5. Roll back application code

Set `AIKYA_FRONTEND_IMAGE` and `AIKYA_BACKEND_IMAGE` to the last approved immutable version/digest, validate Compose again, and run `up -d`. Database rollback uses forward-compatible corrective migrations; never assume `alembic downgrade` is safe.

## CI and branch workflow

Git is the version-control tool; GitHub is the recommended remote host for this solo-founder project. `.github/workflows/ci.yml` runs frontend, backend, Compose, and image-build checks on every push or pull request to `master`. It performs CI only and contains no deployment credentials or CD job.

Recommended flow:

```powershell
git checkout -b feature/<short-name>
git add .
git commit -m "<message>"
git push -u origin feature/<short-name>
```

Open a pull request into `master`, require the Aikya CI checks to pass, then merge. Direct pushes to `master` also trigger CI, but branch protection is safer.

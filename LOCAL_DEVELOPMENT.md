# Aikya AI Native Windows Development

Last updated: 2026-08-02  
Target: Windows 11 + PowerShell, with application code running natively  
Docker requirement: none

This is the canonical Docker-free development workflow. It does not replace or modify the existing Docker workflow. Use only synthetic local data and local-only credentials.

## Audited repository contract

| Area | Repository evidence | Native contract |
|---|---|---|
| Frontend | `frontend/package.json`, `package-lock.json`, `nuxt.config.ts` | Nuxt 4.5.1, Vue 3.5.40, TypeScript 5.9.3, Node.js `>=24.18.0 <25`, npm lockfile v3 |
| Backend | `backend/pyproject.toml`, `uv.lock` | Python `>=3.14`, FastAPI 0.141.1, Uvicorn 0.52.0, SQLAlchemy 2.0.51, Alembic 1.18.5 |
| Python tooling | `uv.lock`, CI workflow | uv with a frozen lock; CI uses uv 0.11.12 and Python 3.14 |
| Worker | `backend/app/worker.py` | Celery 5.6.3 with Redis broker/result backend; native Windows uses the supported `solo` pool |
| Database | Compose, `backend/app/database.py`, Alembic | PostgreSQL 17 on `127.0.0.1:5432`; Alembic migration entry point is `backend/alembic.ini` |
| Cache/queue | Compose and backend settings | Redis on `127.0.0.1:6379`, databases 0/1/2 for app/broker/results |
| Object storage | Compose and storage adapter | S3-compatible MinIO API 9000 and console 9001; three private buckets |
| Malware scanner | Compose and `platform/malware.py` | clamd TCP `INSTREAM` protocol on `127.0.0.1:3310` |

The Docker reference pins PostgreSQL 17, Redis 7.4, MinIO `RELEASE.2025-04-22T22-12-26Z`, and `clamav/clamav:1.4_base`. The native setup script downloads that exact MinIO Windows release and verifies its published SHA-256. Redis and ClamAV are installed from their maintained Ubuntu repositories inside WSL and are validated by protocol, not by an invented version claim.

### Application entry points

| Process | Working directory | Exact entry point |
|---|---|---|
| Nuxt dev server | `frontend/` | `npm.cmd run dev` (pinned to `127.0.0.1:3000`) |
| FastAPI | `backend/` | `.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload` |
| Celery worker | `backend/` | `.venv\Scripts\python.exe -m celery -A app.worker:celery_app worker --loglevel=INFO --pool=solo` |
| Database migration | `backend/` | `.venv\Scripts\python.exe -m alembic upgrade head` |

There is no database seed command, Celery Beat/scheduler entry point, frontend formatter script, or automated test command in the current repository. Do not invent or run one. The scheduler in architecture documents is future topology and is not implemented in Phase 1.

## Native topology and startup order

| Order | Service | Location | Port | Ownership |
|---:|---|---|---:|---|
| 1 | PostgreSQL 17 | Windows service | 5432 | independently managed |
| 2 | Redis | WSL Ubuntu service | 6379 | shared local infrastructure |
| 3 | ClamAV daemon | WSL Ubuntu service | 3310 | shared local infrastructure |
| 4 | MinIO | Windows binary in `tmp/local-dev/tools/` | 9000/9001 | started/stopped by Aikya scripts |
| 5 | MinIO bucket bootstrap | one-shot native Python/boto3 command | - | start script |
| 6 | Alembic migrations | native Python | - | start script |
| 7 | FastAPI | native Python | 8000 | start/stop scripts |
| 8 | Celery worker | native Python, `solo` pool | - | start/stop scripts |
| 9 | Nuxt | native Node.js | 3000 | start/stop scripts |

WSL 2 forwards Linux services to Windows localhost by default. Microsoft documents both [WSL installation](https://learn.microsoft.com/windows/wsl/install) and [localhost networking](https://learn.microsoft.com/windows/wsl/networking). No application source runs in WSL.

## 1. Install host prerequisites

### Git and Node.js

Install Git and Node.js 24.18.x. The frontend rejects Node 25 or Node versions below 24.18.0. Use the [official Node.js download](https://nodejs.org/en/download), then open a new PowerShell window:

```powershell
git --version
node.exe --version
npm.cmd --version
```

Use `npm.cmd`, not `npm`, when Windows execution policy blocks the `npm.ps1` shim.

### uv and Python 3.14

Install uv using its [official Windows package instruction](https://docs.astral.sh/uv/getting-started/installation/):

```powershell
winget install --id=astral-sh.uv -e
uv.exe --version
```

The setup script asks uv to install a compatible Python 3.14 runtime and synchronizes `backend/uv.lock`; a separate global Python installation is not required.

### PostgreSQL 17 for Windows

Install PostgreSQL 17 using the [PostgreSQL Windows installer](https://www.postgresql.org/download/windows/). Keep the server bound to local development interfaces and remember the local `postgres` administrator password. Add the actual installer-selected `bin` directory to your user `PATH`; this guide does not guess an installation directory.

Open `psql` as the local administrator:

```powershell
psql.exe -U postgres -d postgres
```

The native repository contract uses the existing local `postgres` administrator role and database `aikya-ai`. Create only the database if it is missing:

```sql
CREATE DATABASE "aikya-ai";
```

Never drop or recreate an existing database as a setup shortcut. Verify from PowerShell and let `psql` prompt for the password:

```powershell
psql.exe -h localhost -p 5432 -U postgres -d aikya-ai -W -c 'SELECT current_database(), current_user;'
```

### Existing PostgreSQL and pgAdmin installation

pgAdmin is an administration client; the PostgreSQL Windows service is the database server the backend connects to. In pgAdmin, register or open the local server with host `localhost`, port `5432`, maintenance database `postgres`, administrator user `postgres`, and the password selected during PostgreSQL installation. Do not put that administrator password in tracked files.

If the local `postgres` password is not `1234`, either keep the real local password in ignored `.env.local` or deliberately synchronize this development-only machine through **Tools -> Query Tool**:

```sql
ALTER ROLE postgres WITH PASSWORD '1234';
```

If the database does not exist, use **Databases -> Create**, name it `aikya-ai`, and choose `postgres` as owner. The equivalent explicit command is:

```powershell
psql.exe -U postgres -h localhost -p 5432 -c 'CREATE DATABASE "aikya-ai";'
```

The canonical ignored file is `Aikya\.env.local` and its native value is:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:1234@localhost:5432/aikya-ai
```

This machine currently has a PostgreSQL 18 service listening on port 5432. It is reachable, but PostgreSQL 17 remains the repository's tested/pinned baseline; using 18 locally does not change the project contract.

### WSL Ubuntu, Redis, and ClamAV

Redis documents WSL as its Windows path. From an Administrator PowerShell window, install WSL if it is absent, then restart Windows:

```powershell
wsl.exe --install -d Ubuntu
wsl.exe --list --verbose
```

Open Ubuntu once and create its Linux user. Then install Redis from the [official Redis APT repository](https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-redis/install-redis-on-linux/) and ClamAV packages:

```bash
sudo apt-get install -y lsb-release curl gpg
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install -y redis clamav clamav-daemon
```

Configure clamd's TCP protocol for the native Windows worker. `TCPSocket` and `TCPAddr` are the daemon's documented settings; loopback binding avoids LAN exposure:

```bash
sudo systemctl stop clamav-daemon clamav-freshclam || true
sudo freshclam
sudo cp /etc/clamav/clamd.conf /etc/clamav/clamd.conf.aikya-backup
sudo sed -i '/^TCPSocket /d;/^TCPAddr /d;/^StreamMaxLength /d' /etc/clamav/clamd.conf
printf '\nTCPSocket 3310\nTCPAddr 127.0.0.1\nStreamMaxLength 55M\n' | sudo tee -a /etc/clamav/clamd.conf
sudo systemctl enable redis-server clamav-freshclam clamav-daemon
sudo systemctl start redis-server clamav-freshclam clamav-daemon
redis-cli ping
ss -ltn | grep -E ':6379|:3310'
```

If your WSL distribution does not use systemd, replace `systemctl start` with `sudo service redis-server start` and `sudo service clamav-daemon start`. The Aikya start script supports both service managers.

Back in PowerShell, verify forwarding:

```powershell
Test-NetConnection 127.0.0.1 -Port 6379
Test-NetConnection 127.0.0.1 -Port 3310
```

If you chose a non-default WSL distribution, set its exact registered name in `AIKYA_WSL_DISTRIBUTION` inside `.env.local`.

## 2. Run the repository setup

From the repository root in ordinary PowerShell:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup-local.ps1
```

The script:

- validates Node `>=24.18.0 <25`;
- runs `npm.cmd ci` from the committed npm lockfile;
- installs Python 3.14 through uv and runs `uv sync --frozen`;
- creates ignored runtime/log directories;
- creates `.env.local` only when missing and never overwrites an existing file;
- downloads the exact MinIO release pinned by Compose into ignored `tmp/` storage;
- verifies MinIO SHA-256 `2ceb3b3d68bdf1c4def9702cb02c5c8adb235197d1c8f2eaad24136833ab9a57`.

Use the setup script or `npm.cmd ci`, not `npm install`, for a reproducible checkout. `npm ci` installs exactly `frontend/package-lock.json` and replaces the generated dependency tree. The setup script refuses to begin if it can prove that an Aikya Node process is holding frontend native modules open or a Python process/editor extension is using `backend\.venv`.

Review `.env.local`. Change local credentials if desired, but update PostgreSQL and MinIO values consistently. Add `LIBRETRANSLATE_URL` and `LIBRETRANSLATE_API_KEY` only for a trusted LibreTranslate-compatible provider. The empty provider is valid for startup; translation endpoints intentionally return an unconfigured-provider response.

### Configure real Google sign-in (optional)

The Google button is connected to a real OpenID Connect Authorization Code flow; it is not a decorative button. Without credentials it returns safely to `/login` with a configuration message.

1. In [Google Auth Platform](https://console.cloud.google.com/auth/), configure the consent screen for your development project.
2. Create an OAuth client with application type **Web application**.
3. Add this exact local authorized redirect URI:

   ```text
   http://localhost:8000/api/v1/auth/oauth/google/callback
   ```

4. Put only the issued local values in ignored root `.env.local`:

   ```dotenv
   AUTH_GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   AUTH_GOOGLE_CLIENT_SECRET=your-local-client-secret
   AUTH_GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/oauth/google/callback
   ```

5. Restart FastAPI after changing the environment. Never commit the real client secret.

The backend validates state, nonce, PKCE, signature, issuer, audience, expiry, exact callback, and Google's verified-email claim. A verified Google email may link to the matching local Aikya account; conflicting provider identities fail closed. Production must use an owned HTTPS domain and its exact registered callback URL.

### Passkey 2FA on localhost

WebAuthn considers `http://localhost` a development secure context. Keep these native values unless the frontend host changes:

```dotenv
WEBAUTHN_RP_ID=localhost
WEBAUTHN_RP_NAME=Aikya AI
WEBAUTHN_ORIGIN=http://localhost:3000
```

After signing in, open the dashboard's **Account security** panel and select **Enable passkey 2FA**. Windows Hello, a supported device passkey, or a FIDO2 security key can complete enrollment. Save the ten recovery codes when shown: plaintext codes are displayed once, while only keyed hashes are stored. Once enabled, both local-password and Google sign-in require the registered passkey or one unused recovery code.

## 3. Start all application processes

Ensure the PostgreSQL Windows service is running. Then run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-local.ps1
```

The script imports `.env.local` into child-process environments, verifies PostgreSQL/Redis/ClamAV, starts the pinned MinIO process, creates missing private buckets, applies Alembic migrations, and starts FastAPI, the Windows-safe Celery solo worker, and Nuxt. It never calls Docker.

Before using the full-stack start script, stop any Nuxt process started manually in another terminal. The script checks for Aikya Node processes across all ports-not only 3000-and refuses to start a second process that would share `.nuxt`/`.output`.

Runtime state and logs are ignored by Git:

```text
tmp/local-dev/processes.json
tmp/local-dev/minio-data/
logs/local-dev/frontend.*.log
logs/local-dev/backend.*.log
logs/local-dev/worker.*.log
logs/local-dev/minio.*.log
```

Follow logs:

```powershell
Get-Content .\logs\local-dev\backend.out.log -Wait
Get-Content .\logs\local-dev\worker.out.log -Wait
Get-Content .\logs\local-dev\frontend.out.log -Wait
```

## 4. Verify health and open the application

| Surface | URL or check |
|---|---|
| Nuxt application | `http://localhost:3000` |
| Nuxt health | `http://localhost:3000/healthz` |
| FastAPI docs | `http://127.0.0.1:8000/api/docs` |
| FastAPI liveness | `http://127.0.0.1:8000/health/live` |
| FastAPI readiness | `http://127.0.0.1:8000/health/ready` |
| MinIO API health | `http://127.0.0.1:9000/minio/health/live` |
| MinIO console | `http://127.0.0.1:9001` |

```powershell
Invoke-RestMethod http://localhost:3000/healthz
Invoke-RestMethod http://127.0.0.1:8000/health/live
Invoke-RestMethod http://127.0.0.1:8000/health/ready
```

The backend readiness endpoint checks PostgreSQL. Redis, MinIO, and ClamAV are separately verified by `start-local.ps1` before application startup.

Successful browser login navigates to `http://localhost:3000/app/dashboard` (or its locale-prefixed equivalent). Calling FastAPI's `/api/v1/auth/login` directly in Swagger returns JSON by design; the Nuxt client performs browser navigation after storing the short-lived access token in memory. The long-lived rotating refresh credential remains in an HttpOnly cookie.

## 5. Stop safely

Stop only processes owned by the Aikya scripts:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\stop-local.ps1
```

This stops Nuxt, FastAPI, Celery, and the script-started MinIO after validating recorded PID start times. It preserves PostgreSQL, Redis, ClamAV, database records, object data, and all Docker resources.

To also stop the shared WSL Redis and ClamAV services:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\stop-local.ps1 -IncludeSharedInfrastructure
```

PostgreSQL remains an independently managed Windows service and is never stopped by repository scripts.

## Manual application commands

FastAPI and Alembic automatically read the absolute root `.env.local`; process environment variables override it. The lifecycle scripts remain recommended because they also load the same file for Nuxt, Redis, MinIO, and ClamAV. For focused debugging, explicit temporary overrides use shell-specific syntax:

CMD:

```bat
set DATABASE_URL=postgresql+psycopg://postgres:1234@localhost:5432/aikya-ai
uv run alembic upgrade head
```

PowerShell:

```powershell
$env:DATABASE_URL="postgresql+psycopg://postgres:1234@localhost:5432/aikya-ai"
uv run alembic upgrade head
Remove-Item Env:DATABASE_URL
```

Git Bash:

```bash
export DATABASE_URL="postgresql+psycopg://postgres:1234@localhost:5432/aikya-ai"
uv run alembic upgrade head
unset DATABASE_URL
```

To import every native setting into a PowerShell terminal:

```powershell
Get-Content .\.env.local | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith('#')) {
        $name, $value = $line -split '=', 2
        $value = $value.Trim().Trim('"').Trim("'")
        [Environment]::SetEnvironmentVariable($name.Trim(), $value, 'Process')
    }
}
```

Then use the repository entry points directly.

Frontend:

```powershell
Set-Location frontend
npm.cmd ci
npm.cmd run lint
npm.cmd run typecheck
npm.cmd run dev
```

Backend API:

```powershell
Set-Location backend
uv.exe sync --frozen --python 3.14
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Inspect the effective database target safely, test connectivity, apply migrations, and list created tables:

```powershell
Set-Location backend
.\.venv\Scripts\python.exe -m scripts.database_config
.\.venv\Scripts\python.exe -m scripts.database_config --check
uv.exe run alembic current
uv.exe run alembic upgrade head
uv.exe run alembic current
.\.venv\Scripts\python.exe -m scripts.database_config --check --tables
```

Worker in a separate terminal:

```powershell
Set-Location backend
.\.venv\Scripts\python.exe -m celery -A app.worker:celery_app worker --loglevel=INFO --pool=solo
```

Celery 5.6 documents `solo` as sequential main-thread execution and specifically recommends `solo` or `threads` for Windows spawn issues. `solo` preserves the Phase 1 concurrency value of one and avoids pretending the Linux prefork command is portable.

## Repository quality commands

Frontend:

```powershell
Set-Location frontend
npm.cmd run lint
npm.cmd run typecheck
npm.cmd run build
```

Backend, matching CI:

```powershell
Set-Location backend
uv.exe run ruff check .
uv.exe run mypy app
uv.exe run python -m compileall -q app alembic
uv.exe run alembic heads
```

No `npm test`, pytest suite, E2E suite, or formatting script exists in the current repository. Ruff is installed, but CI defines lint rather than an auto-format operation; do not claim a formatter check passed unless one is formally added and run.

## Environment ownership

`backend/app/config.py` reads the absolute ignored root `.env.local`, so behavior does not depend on whether the command starts in the root or `backend/`. Configuration precedence is: explicit settings arguments, process environment, root `.env.local`, then safe source defaults. `backend/alembic/env.py` replaces the `alembic.ini` placeholder with that same application setting. Compose-injected process values therefore keep priority in Docker.

| Consumer | Native values that differ from Docker |
|---|---|
| Nuxt | `NUXT_API_PROXY_TARGET=http://127.0.0.1:8000`; ports/site URL use 127.0.0.1 |
| FastAPI/Alembic | `DATABASE_URL` points to `localhost:5432`, never the Compose hostname `postgres` |
| Rate limits/Celery | Redis URLs point to `127.0.0.1:6379`, never `redis` |
| Storage | Internal/public endpoints both point to `127.0.0.1:9000`, never `minio` |
| Scanner | `CLAMAV_HOST=127.0.0.1`, never `clamav` |

`.env.local.example` is the complete Phase 1 native template. Root `.env.example` remains the Docker contract. Real `.env.local`, `.env`, logs, caches, virtual environments, runtime state, MinIO data, provider keys, and credentials are ignored and must never be committed.

## Troubleshooting

- `npm.ps1 cannot be loaded`: use `npm.cmd` as the scripts do; no machine-wide execution-policy change is necessary.
- Frontend port mismatch: native Aikya is pinned to `http://localhost:3000`. Stop stale Nuxt processes before changing/restarting the port; `npm.cmd run dev` and `scripts/start-local.ps1` both use 3000.
- Frontend install is corrupt or locked: `Cannot find module './rolldown-runtime-*.mjs'` from Shiki means the generated dependency tree is incomplete. An `EPERM ... unlink ... lightningcss...node` error means an Aikya Node/Nuxt process still owns a Windows native module. From the repository root, first run `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\stop-local.ps1` and close any manually started Aikya `npm`/Nuxt terminal. Do not blindly terminate unrelated Node applications. Once no Aikya frontend process is running, remove only the reproducible `frontend\node_modules` and `frontend\.nuxt` directories, then run `Set-Location frontend` followed by `npm.cmd ci`.
- npm deprecation notices: Aikya no longer directly uses deprecated `lucide-vue-next`; icon imports use `@lucide/vue`. A `vue-i18n@10` notice currently comes through `@nuxtjs/i18n -> @intlify/unplugin-vue-i18n -> @intlify/vue-i18n-extensions`, and `glob@10` comes through Nuxt/Nitro's archive tooling. They are upstream transitive notices, not separately installed Aikya packages. Do not add forced npm overrides merely to hide them; review them when compatible upstream releases change the dependency ranges. `npm.cmd audit` is the security check.
- PostgreSQL port closed: start the PostgreSQL 17 Windows service selected during installation; scripts do not guess its service name.
- Database authentication failure: verify `DATABASE_URL` matches the role/database actually created. Do not drop local data as a first fix.
- `failed to resolve host 'postgres'`: `postgres` is a Docker-internal service name. Native Windows commands must use the root `.env.local` value with host `localhost`. Run `python -m scripts.database_config` from `backend/` to confirm the masked effective target.
- Database `aikya-ai` does not exist: create it explicitly through pgAdmin or `psql.exe -U postgres -h localhost -p 5432 -c 'CREATE DATABASE "aikya-ai";'`, then run the existing Alembic migration. No new migration is required.
- `uv sync` cannot replace `.venv` or reports access denied: a backend, worker, debugger, or VS Code Python formatter is using the virtual environment. Stop only those Aikya processes or run **Developer: Reload Window** in VS Code, then rerun `setup-local.ps1`. The setup preflight reports the relevant Python PID instead of partially replacing the environment.
- Redis/ClamAV unavailable: run `wsl.exe`, then `sudo systemctl status redis-server clamav-daemon`; confirm ports with `ss -ltn`.
- ClamAV has no database: run `sudo freshclam` in WSL, then restart `clamav-daemon`.
- MinIO fails hash verification: do not bypass verification. Remove only `tmp/local-dev/tools/minio.exe` and rerun setup on a trusted network.
- Stale process state: run `stop-local.ps1`. It validates PID start times before stopping anything.
- Port conflict: change the corresponding port and every URL that refers to it in `.env.local`; the default values come from the actual repository configuration.
- Translation returns 503: configure a trusted `LIBRETRANSLATE_URL`; this is expected when the provider is blank.

## Clean-machine source links

- [Node.js downloads](https://nodejs.org/en/download)
- [uv Windows installation](https://docs.astral.sh/uv/getting-started/installation/)
- [PostgreSQL Windows installer](https://www.postgresql.org/download/windows/)
- [Microsoft WSL installation](https://learn.microsoft.com/windows/wsl/install)
- [Redis on Windows/WSL](https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-redis/install-redis-on-windows/)
- [ClamAV installation](https://docs.clamav.net/manual/Installing.html)
- [MinIO Windows standalone server](https://min.io/docs/minio/windows/operations/install-deploy-manage/deploy-minio-single-node-single-drive.html)
- [Celery concurrency pools](https://docs.celeryq.dev/en/stable/userguide/concurrency/index.html)

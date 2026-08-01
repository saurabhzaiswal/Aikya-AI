# Aikya AI

## One World. One Understanding.

Aikya AI is a privacy-first language-intelligence platform for translating and understanding documents, images, websites, and real-world text while preserving structure and context as much as the source format allows.

This repository contains the implemented **Phase 1 MVP application** and its engineering foundation. The current web product supports secure local accounts, a personal dashboard, plain-text translation, and asynchronous translation of digital PDFs into a readable downloadable PDF. Docker/provider runtime acceptance and beta security work remain before release.

## Vision

Aikya aims to become the most trusted place to understand information across languages. The product combines translation, OCR, document intelligence, comparison, optional AI assistance, and speech in one controlled workflow.

Key principles:

- Preserve structure and communicate fidelity honestly.
- Keep private documents tenant-isolated and user-controlled.
- Make AI enhancement explicit and optional.
- Build a web-first modular monolith before expanding clients or services.
- Treat accessibility, localization, observability, testing, and deletion as product requirements.

## Phase 1 capabilities

- Registration, login, rotating refresh sessions, logout, and personal workspace isolation.
- Plain-text translation through a configurable LibreTranslate-compatible provider, with history.
- Signed private PDF upload, checksum/signature/page validation, malware scanning, embedded-text extraction, asynchronous translation, progress, and readable PDF export.
- Nuxt 4 SSR public website and client-rendered dashboard, dark mode, keyboard-visible controls, safe error states, and explicit scanned-PDF/layout limitations.

## Planned capabilities

- Plain-text and document translation.
- DOCX, PDF, image/scanned-document processing, followed by PPTX, XLSX, HTML, Markdown, and EPUB.
- Layout-aware reconstruction and readable fallback outputs.
- OCR, side-by-side comparison, resume workflows, optional AI explanation/improvement, and audio.
- Browser extension, mobile and desktop clients.
- Organizations, teams, usage, billing, API keys, audit logs, and enterprise controls.

The next private-beta gate is intentionally narrower than the long-term vision: harden the implemented web/text/digital-PDF flow, add active deletion/retention automation, automated critical-path coverage, and complete deployment/security drills. OCR and DOCX remain future scope.

## Architecture overview

Aikya begins as a modular FastAPI monolith backed by PostgreSQL. Celery workers independently scale document, OCR, translation, and render workloads. Redis handles transient queue/cache/rate-limit concerns. Private S3-compatible storage holds immutable source, intermediate, and output objects. The core format-neutral Document IR allows parsers, translation, comparison, and renderers to evolve independently.

See the [technical architecture](docs/04-architecture.md) and editable [architecture diagrams](docs/diagrams/).

## Technology stack

- Web: Node.js 24.18.x, Nuxt 4, Vue 3 Options API for stateful UI, TypeScript, Pinia, Nuxt i18n, Tailwind CSS, SCSS, Nuxt Content, and structured SEO metadata.
- Backend: Python 3.14+, FastAPI, SQLAlchemy, Alembic, and application-generated UUIDv7 entity identifiers.
- Data: PostgreSQL, Redis, S3-compatible object storage.
- Jobs: Celery with durable PostgreSQL state and transactional outbox.
- Phase 1 documents: PyMuPDF for embedded-text extraction and readable PDF output; ClamAV for upload scanning.
- Providers: adapter-based translation, OCR, AI, speech, OAuth, email, and payment integrations.
- Delivery: Docker, Nuxt Nitro, Nginx/edge, CI/CD, metrics, logs, traces, and error tracking.
- Later clients: Vue + Vite extension, Tauri desktop, and Capacitor mobile applications; none are part of Phase 1.

## Repository structure

```text
docs/                 Product and engineering source of truth
docs/decisions/       Architecture decision records
docs/diagrams/        Editable Excalidraw sources
frontend/             Unified Nuxt 4 public website and Phase 1 workspace
backend/              FastAPI API, migrations, and Celery worker
docker/               Local and reference production container topology
development.md        Local environment and engineering workflow
.env.example          Safe configuration contract
compose.yaml          Root development Compose entry point
RUNBOOK.md             Canonical laptop/production operating commands
```

## Development environment

Requirements: Docker Engine/Desktop with Docker Compose v2 and Git. No Python, Node.js, PostgreSQL, Redis, or MinIO installation is required on the host. Native checks use Node.js 24.18.x and Python 3.14+.

```text
copy .env.example .env
docker compose up -d
docker compose ps
```

The stack builds the Nuxt frontend, FastAPI backend, Celery worker, PostgreSQL, Redis, private MinIO storage, and ClamAV scanner. Configure `LIBRETRANSLATE_URL` in the ignored `.env` before using translation. See [development.md](development.md) for commands, ports, and known runtime prerequisites.

Never use `.env.example` values in production. See the canonical [local and production runbook](RUNBOOK.md) for startup, verification, shutdown, production rehearsal, rollback, and CI workflow.

## Documentation

Start with the [documentation index](docs/README.md). The foundation includes product vision, traceable requirements, roadmap, architecture, data model, API planning, UX, security, deployment, testing, business, pricing, brand, and editable diagrams.

## Roadmap

1. Complete Docker runtime acceptance with a real translation provider.
2. Add deletion/retention automation, automated critical-flow coverage, and security/restore drills.
3. Harden an invite-only web beta using the current text and digital-PDF scope.
4. Evaluate richer document fidelity, formats, and OCR only after Phase 1 evidence.
5. Expand comparison/resume, extension, billing, AI/audio, API/enterprise, and other clients based on evidence.

Detailed gates and estimates are in the [roadmap](docs/03-roadmap.md).

## Current status

The Phase 1 backend and synthetic API/worker flows pass their existing checks. The Nuxt 4 migration passes lint and typecheck; client/SSR compilation, 31-route prerendering, and generated-server HTTP/SEO smoke checks pass. Final Nitro dependency tracing exceeded the local Windows build timeout, so container packaging remains open. Full Compose runtime, real-provider/MinIO/ClamAV integration, browser visual QA, automated suites, active deletion/retention, and the final security review also remain open; the repository is not production-ready.

## Founder

Built and maintained by **Saurabh Choudhary**, founder and solo developer.

- [LinkedIn](https://www.linkedin.com/in/saurabh-choudhary-7ab207239/)
- [GitHub](https://github.com/saurabhzaiswal)
- [Dev Community](https://dev.to/saurabhzaiswal)
- [Portfolio](https://saurabhzaiswal.vercel.app/)

Aikya AI is an independent SaaS project focused on removing language barriers through intelligent document and language technology. Public profiles are used only for attribution and contact.

## License

Copyright © 2026 Saurabh Choudhary. All rights reserved. See [LICENSE](LICENSE).

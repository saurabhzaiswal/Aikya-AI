# Phase 1 MVP Feature Specification

## Problem

Users need a trustworthy way to translate plain text and digital PDFs without manual extraction and without losing access to a downloadable result.

## User stories

- As a user, I can create an account and return to my private history.
- I can translate text through a configured translation provider.
- I can upload a supported digital PDF, choose a target language, see durable processing state, and download a readable translated PDF.
- I can understand limitations and errors without my content appearing in logs.

## Scope

Authentication, personal tenancy/workspace, dashboard, text translation/history, signed PDF upload, validation, asynchronous extraction/translation/render, job status, and authorized output download.

## Non-goals

OCR/scanned PDF translation, layout-perfect reconstruction, DOCX, AI enhancement, audio, billing, teams, public API, extension, mobile, desktop, and enterprise functions.

## Technical design

Vue Options API client calls `/api/v1`. FastAPI modules own identity/users/organizations, documents/storage/jobs, and translation. PostgreSQL persists state. Redis/Celery executes PDF processing. MinIO/S3 stores private immutable binaries. PyMuPDF extracts embedded text and creates a basic readable translated PDF; low/no embedded text produces `ocr_required`, not a fake result.

## Security and privacy

Use secure rotating sessions, tenant authorization, direct quarantine upload, signature/size/checksum/page validation, fail-closed malware scanning, randomized object keys, short signed download, content-free logs, and bounded provider requests. PDF parsing runs in a worker with resource limits in production. Active deletion/retention automation is a mandatory private-beta follow-up and is not claimed by the first implementation cut.

## UX

The dashboard presents Text and PDF workflows, recent work, real processing stages, warnings, retry guidance, and export. Dark mode, keyboard access, visible focus, reduced motion, responsive layout, and meaningful status text are required.

## Verification

Current founder instruction defers automated suites. Required evidence: dependency install/lock, TypeScript and production frontend build, backend import/static/compile and Alembic upgrade checks, Compose configuration, and manual/smoke register → login → translate text → upload supported PDF → process → download where runtime/provider access permits.

Implementation is complete for the first cut. Static/build/migration and synthetic critical-flow checks pass; complete Docker/provider runtime acceptance, visual QA, deletion/retention, automated suites, and final security review remain open.

## Future improvements

Document IR fidelity, richer page reconstruction, OCR, progress streaming, glossary/memory, DOCX and more formats. These do not enter Phase 1 implicitly.

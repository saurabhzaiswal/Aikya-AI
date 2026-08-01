# ADR-002: Use FastAPI for the Backend

Date: 2026-08-01  
Status: Accepted  
Decision authority: Founder

## Context

Aikya requires HTTP APIs, authentication, asynchronous document orchestration, PostgreSQL access, and deep integration with Python document, OCR, and language libraries.

## Options considered

1. Python + FastAPI.
2. Django/DRF.
3. Node.js backend.
4. Multiple specialized services from the beginning.

## Decision

Use Python and FastAPI with SQLAlchemy, Alembic, PostgreSQL, Redis, and Celery. Keep domain/application logic independent from framework and vendor SDKs.

## Reason

Python provides the required document/OCR/AI ecosystem; FastAPI provides typed API contracts and a lightweight composition model suitable for a modular monolith.

## Consequences

- Python packaging, typing, migration, linting, and ASGI operations become core practices.
- CPU/blocking document work cannot run in request handlers and moves to workers.
- FastAPI schemas generate the OpenAPI contract and typed frontend client.
- A later framework change would be costly and requires a superseding ADR.

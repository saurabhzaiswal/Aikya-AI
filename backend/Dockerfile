# syntax=docker/dockerfile:1.7

FROM python:3.14-slim AS runtime-base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN groupadd --system aikya && useradd --system --gid aikya --create-home aikya
WORKDIR /app

FROM runtime-base AS production-dependencies
COPY --from=ghcr.io/astral-sh/uv:0.8.4 /uv /uvx /bin/
COPY pyproject.toml uv.lock* ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

ENV PATH="/app/.venv/bin:$PATH"

FROM production-dependencies AS development
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project
COPY --chown=aikya:aikya app ./app
COPY --chown=aikya:aikya alembic ./alembic
COPY --chown=aikya:aikya alembic.ini ./alembic.ini
USER aikya
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM runtime-base AS production
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=production-dependencies --chown=aikya:aikya /app/.venv /app/.venv
COPY --chown=aikya:aikya app ./app
COPY --chown=aikya:aikya alembic ./alembic
COPY --chown=aikya:aikya alembic.ini ./alembic.ini
USER aikya
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]

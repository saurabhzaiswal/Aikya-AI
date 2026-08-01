FROM python:3.14-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN groupadd --system aikya && useradd --system --gid aikya --create-home aikya
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.8.4 /uv /uvx /bin/
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev --no-install-project

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
RUN uv sync --frozen --no-dev

USER aikya
ENV PATH="/app/.venv/bin:$PATH"

FROM base AS development
USER root
RUN uv sync --frozen
USER aikya
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM base AS production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]

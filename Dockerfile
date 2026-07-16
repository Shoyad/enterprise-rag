# Slim image built with uv. First built at Milestone 2 (bootstrap), when src/app has
# an entrypoint. Committed at Milestone 1 as the container strategy.
FROM python:3.12-slim

# uv: fast, reproducible dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Dependency layer (cached independently of source)
COPY pyproject.toml ./
RUN uv sync --no-install-project --extra dev

# Application source
COPY src ./src
COPY migrations ./migrations
RUN uv sync --extra dev

ENV PYTHONPATH=/app/src

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

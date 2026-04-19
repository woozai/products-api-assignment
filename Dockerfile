FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.10.7 /uv /uvx /usr/local/bin/

# Copy dependency files first so Docker can reuse this layer when app code changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

COPY app ./app
COPY run.py ./

EXPOSE 8000

CMD ["uv", "run", "flask", "--app", "run", "run", "--host", "0.0.0.0", "--port", "8000"]

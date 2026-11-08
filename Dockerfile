FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl unzip ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.12 /uv /bin/uv
COPY --from=oven/bun:1 /usr/local/bin/bun /usr/local/bin/bun

WORKDIR /app
COPY . .
RUN uv venv && uv pip install -r requirements.txt
RUN uv run reflex export --frontend-only --no-zip

EXPOSE 3000
CMD ["sh", "-c", "exec uv run reflex run --env prod --single-port --frontend-port 3000 --loglevel debug"]
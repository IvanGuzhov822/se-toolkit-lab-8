ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0
ENV UV_HTTP_TIMEOUT=600

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY nanobot/pyproject.toml ./nanobot/pyproject.toml
COPY mcp/mcp-lms/pyproject.toml ./mcp/mcp-lms/pyproject.toml
COPY nanobot-websocket-channel/nanobot-webchat/pyproject.toml ./nanobot-websocket-channel/nanobot-webchat/pyproject.toml
COPY nanobot-websocket-channel/mcp-webchat/pyproject.toml ./nanobot-websocket-channel/mcp-webchat/pyproject.toml
COPY nanobot-websocket-channel/nanobot-channel-protocol/pyproject.toml ./nanobot-websocket-channel/nanobot-channel-protocol/pyproject.toml

COPY nanobot ./nanobot
COPY mcp/mcp-lms ./mcp/mcp-lms
COPY nanobot-websocket-channel/nanobot-webchat ./nanobot-websocket-channel/nanobot-webchat
COPY nanobot-websocket-channel/mcp-webchat ./nanobot-websocket-channel/mcp-webchat
COPY nanobot-websocket-channel/nanobot-channel-protocol ./nanobot-websocket-channel/nanobot-channel-protocol

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package nanobot

FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER nonroot

WORKDIR /app/nanobot

CMD ["python", "/app/nanobot/entrypoint.py"]

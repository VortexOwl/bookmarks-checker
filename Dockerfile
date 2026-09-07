FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

COPY .python-version LICENSE README.md ./
COPY src/ ./src/
COPY data/ ./data/

RUN uv sync --frozen

VOLUME ["/app/data"]

CMD ["uv", "run", "web"]
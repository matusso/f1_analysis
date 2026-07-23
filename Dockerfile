FROM python:3.12-slim

# uv binary from the official distroless image (pinned for reproducibility).
COPY --from=ghcr.io/astral-sh/uv:0.11.31 /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    F1_CACHE_DIR=/data/f1cache

WORKDIR /app

# 1) Install dependencies from the lockfile first (cached unless the lock
#    changes). --no-install-project keeps the project out of this layer.
COPY pyproject.toml uv.lock README.md ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# 2) Add the source and install the project itself.
COPY src ./src
COPY streamlit_app.py ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Put the project's virtualenv on PATH so `streamlit` resolves directly.
ENV PATH="/app/.venv/bin:${PATH}"

RUN mkdir -p /data/f1cache
EXPOSE 8501

# Basic container health signal for orchestrators.
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", \
    "--server.port=8501", "--server.address=0.0.0.0"]

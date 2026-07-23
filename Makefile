.PHONY: install dev run lint format typecheck test check lock export docker

# Sync the runtime environment from the lockfile (no dev tooling).
install:
	uv sync --frozen --no-dev

# Full dev environment: dev group (default) + the grafana feature extra.
dev:
	uv sync --extra grafana

run:
	uv run streamlit run streamlit_app.py

lint:
	uv run ruff check src tests

format:
	uv run ruff format src tests

typecheck:
	uv run mypy src

test:
	uv run pytest

check: lint typecheck test

# Refresh uv.lock, then regenerate the pip-compatible requirements.txt.
lock:
	uv lock

export:
	uv export --no-hashes --no-dev --format requirements-txt -o requirements.txt

docker:
	docker build -t f1-analysis .

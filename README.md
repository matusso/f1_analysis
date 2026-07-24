# F1 Analysis

Formula 1 telemetry analysis and comparison, delivered as a [Streamlit](https://streamlit.io/)
application built on [FastF1](https://docs.fastf1.dev/).

Pick a season, circuit and session, then compare two drivers' laps across speed,
gear, RPM, throttle, brake and DRS channels, inspect sector-time deltas and raw
lap data, and view qualifying classifications.

## Architecture

The project is an installable Python package with a clean layered structure, so
the FastF1 data layer, the chart layer, and the Streamlit UI evolve
independently — and new output backends (e.g. Grafana) plug in without touching
the rest.

```
src/f1_analysis/
├── config.py            # env-driven settings (pydantic-settings)
├── data/                # FastF1 access + typed domain models
│   ├── loader.py        # the only module that imports FastF1
│   └── models.py        # DriverRef, LapSectors
├── viz/                 # Plotly figure construction
│   └── telemetry.py
├── exporters/           # pluggable output backends (extension point)
│   ├── base.py          # Exporter ABC + ExportPayload
│   ├── registry.py      # name-based registry
│   └── grafana.py       # planned Grafana backend (scaffolded)
└── app/                 # Streamlit presentation layer
    ├── main.py          # entry point (status-bar dropdowns select the dashboard)
    ├── cli.py           # `f1-analysis` console script
    ├── widgets.py       # shared driver/lap selector
    └── views/           # one module per dashboard: telemetry, results
streamlit_app.py         # repo-root launcher (Streamlit Cloud convention)
tests/                   # pytest suite
```

## Getting started

Requires Python **3.10+**. The project uses [uv](https://docs.astral.sh/uv/) for
dependency management (a `uv.lock` pins the full, reproducible environment).

```bash
# Install uv once (see https://docs.astral.sh/uv/getting-started/installation/):
# curl -LsSf https://astral.sh/uv/install.sh | sh

uv sync                       # creates .venv from uv.lock (incl. dev tools)
uv run streamlit run streamlit_app.py
```

Or with the installed console script:

```bash
uv run f1-analysis
```

Not using uv? A pip-compatible, fully pinned `requirements.txt` is generated
from the lockfile:

```bash
pip install -r requirements.txt   # installs deps + the app package (-e .)
streamlit run streamlit_app.py
```

FastF1 downloads and caches session data on first use (into `.f1cache/` by
default).

## Configuration

All settings are environment variables with the `F1_` prefix (see
[`.env.example`](.env.example)); copy it to `.env` to override defaults.

| Variable          | Default      | Purpose                              |
| ----------------- | ------------ | ------------------------------------ |
| `F1_CACHE_DIR`    | `.f1cache`   | FastF1 on-disk cache directory       |
| `F1_APP_TITLE`    | `F1 Analysis`| Page title                           |
| `F1_APP_LAYOUT`   | `wide`       | Streamlit layout                     |
| `F1_GRAFANA_*`    | unset        | Reserved for the Grafana exporter    |

## Development

```bash
make dev         # uv sync with the grafana extra (dev group is default)
make run         # launch the app
make check       # ruff + mypy + pytest (all via `uv run`)
make lock        # refresh uv.lock after changing dependencies
make export      # regenerate requirements.txt from the lockfile
```

Dependencies are declared in `pyproject.toml`: runtime deps under `[project]`,
the optional `grafana` feature under `[project.optional-dependencies]`, and dev
tooling in the PEP 735 `[dependency-groups]` table (installed by default on
`uv sync`). After editing them, run `make lock && make export` and commit both
`uv.lock` and `requirements.txt`.

## Extending: export backends

`src/f1_analysis/exporters` is the extension point for shipping analysis data to
external systems. Implement the `Exporter` contract and register it:

```python
from f1_analysis.exporters import Exporter, ExportPayload, register

@register
class CsvExporter(Exporter):
    name = "csv"

    def export(self, payload: ExportPayload) -> None:
        ...
```

The **Grafana** backend (`exporters/grafana.py`) is scaffolded and registered;
its `export()` is a stub pending the choice of Grafana data source. Its
`requests` dependency lives under the optional `grafana` extra
(`uv sync --extra grafana`).

## Deployment

- **Docker**: `docker build -t f1-analysis . && docker run -p 8501:8501 f1-analysis`
- **Streamlit Community Cloud**: point it at `streamlit_app.py`; it installs from
  `requirements.txt`.

## Dependencies

The source of truth is [`pyproject.toml`](pyproject.toml) (compatible ranges) +
[`uv.lock`](uv.lock) (the exact resolved, cross-platform environment).
[`requirements.txt`](requirements.txt) is **generated** from the lockfile via
`uv export` for pip/Streamlit-Cloud consumers — edit dependencies in
`pyproject.toml`, not there. Pins track FastF1 3.8's own constraints (notably
`pandas<3.0`).

"""Application configuration.

All settings are environment-driven (12-factor style) with sensible defaults so
the app runs out of the box. Override any field with an ``F1_``-prefixed
environment variable, e.g. ``F1_CACHE_DIR=/var/cache/fastf1``.

The ``grafana_*`` fields are placeholders for the planned Grafana export module
(see :mod:`f1_analysis.exporters`); they are unused until that backend ships.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed, validated application settings."""

    model_config = SettingsConfigDict(
        env_prefix="F1_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Data / FastF1 -----------------------------------------------------
    cache_dir: Path = Field(
        default=Path(".f1cache"),
        description="Directory FastF1 uses to cache downloaded session data.",
    )
    available_years: tuple[int, ...] = Field(
        default=(2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026),
        description="Seasons offered in the year selector.",
    )

    # --- Presentation ------------------------------------------------------
    app_title: str = Field(default="F1 Analysis")
    app_layout: str = Field(default="wide")

    # --- Grafana export (future backend; see exporters/) -------------------
    grafana_url: str | None = Field(default=None)
    grafana_api_key: str | None = Field(default=None)
    grafana_org_id: int | None = Field(default=None)

    def ensure_cache_dir(self) -> Path:
        """Create the cache directory if needed and return its absolute path."""
        path = self.cache_dir.expanduser().resolve()
        path.mkdir(parents=True, exist_ok=True)
        return path


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide, cached settings instance."""
    return Settings()

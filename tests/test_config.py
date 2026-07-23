"""Tests for application settings."""

from pathlib import Path

from f1_analysis.config import Settings


def test_defaults():
    settings = Settings()
    assert settings.app_title == "F1 Analysis"
    assert 2024 in settings.available_years
    assert settings.grafana_url is None


def test_env_override(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("F1_CACHE_DIR", str(tmp_path / "cache"))
    monkeypatch.setenv("F1_APP_TITLE", "Custom")
    settings = Settings()
    assert settings.app_title == "Custom"
    resolved = settings.ensure_cache_dir()
    assert resolved.exists()
    assert resolved.is_dir()

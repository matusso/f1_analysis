"""Tests for the exporter registry and Grafana backend scaffolding."""

import pytest

from f1_analysis.exporters import (
    Exporter,
    ExportError,
    ExportPayload,
    available,
    get_exporter,
    register,
)


def test_grafana_is_registered():
    assert "grafana" in available()


def test_unknown_exporter_raises():
    with pytest.raises(KeyError):
        get_exporter("does-not-exist")


def test_grafana_requires_configuration():
    exporter = get_exporter("grafana", url=None, api_key=None)
    payload = ExportPayload(name="test", rows=[{"a": 1}])
    with pytest.raises(ExportError):
        exporter.export(payload)


def test_custom_exporter_roundtrip():
    calls: list[ExportPayload] = []

    @register
    class _Memory(Exporter):
        name = "memory-test"

        def export(self, payload: ExportPayload) -> None:
            calls.append(payload)

    exporter = get_exporter("memory-test")
    payload = ExportPayload(name="p", rows=[{"x": 1}], metadata={"season": 2024})
    exporter.export(payload)
    assert calls == [payload]

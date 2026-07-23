"""Grafana export backend (planned).

This is the scaffolding for pushing analysis datasets into Grafana — the
intended path is a Grafana-managed data source (e.g. an Infinity/JSON endpoint
or a time-series push). The class is registered and fully typed so the app can
already offer it in a selector, but :meth:`export` is intentionally a stub until
the backing data source is chosen and wired up.

Configuration comes from :class:`f1_analysis.config.Settings` (``F1_GRAFANA_*``
env vars): ``grafana_url``, ``grafana_api_key``, ``grafana_org_id``.
"""

from __future__ import annotations

from f1_analysis.config import get_settings
from f1_analysis.exporters.base import Exporter, ExportError, ExportPayload
from f1_analysis.exporters.registry import register


@register
class GrafanaExporter(Exporter):
    """Push analysis payloads to Grafana (not yet implemented)."""

    name = "grafana"

    def __init__(
        self,
        url: str | None = None,
        api_key: str | None = None,
        org_id: int | None = None,
    ) -> None:
        settings = get_settings()
        self.url = url or settings.grafana_url
        self.api_key = api_key or settings.grafana_api_key
        self.org_id = org_id or settings.grafana_org_id

    @property
    def is_configured(self) -> bool:
        return bool(self.url and self.api_key)

    def export(self, payload: ExportPayload) -> None:  # noqa: D102 - see class docstring
        if not self.is_configured:
            raise ExportError(
                "Grafana export is not configured. Set F1_GRAFANA_URL and "
                "F1_GRAFANA_API_KEY."
            )
        # TODO: implement the actual push once the Grafana data source is chosen.
        # The `requests` dependency ships under the optional [grafana] extra.
        raise ExportError(
            f"Grafana export backend is not implemented yet "
            f"(payload '{payload.name}', {len(payload.rows)} rows)."
        )

"""Visualization layer: builds Plotly figures from FastF1 telemetry."""

from f1_analysis.viz.telemetry import TELEMETRY_CHANNELS, TelemetryChannel, compare_channel

__all__ = ["TELEMETRY_CHANNELS", "TelemetryChannel", "compare_channel"]

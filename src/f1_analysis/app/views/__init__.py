"""Streamlit view renderers, one module per dashboard."""

from f1_analysis.app.views.results import render_results
from f1_analysis.app.views.telemetry import render_telemetry

__all__ = ["render_results", "render_telemetry"]

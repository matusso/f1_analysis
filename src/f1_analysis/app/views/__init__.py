"""Streamlit view renderers, one module per tab."""

from f1_analysis.app.views.results import render_results
from f1_analysis.app.views.stats import render_stats
from f1_analysis.app.views.telemetry import render_telemetry

__all__ = ["render_results", "render_stats", "render_telemetry"]

"""F1 Analysis — Formula 1 telemetry analysis and comparison.

Public package layout:

* :mod:`f1_analysis.config`     — application settings (env-driven).
* :mod:`f1_analysis.data`       — FastF1 session access and typed models.
* :mod:`f1_analysis.viz`        — chart construction (Plotly figures).
* :mod:`f1_analysis.exporters`  — pluggable output backends (e.g. Grafana).
* :mod:`f1_analysis.app`        — the Streamlit presentation layer.
"""

__version__ = "1.0.0"

__all__ = ["__version__"]

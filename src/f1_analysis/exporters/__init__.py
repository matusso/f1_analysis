"""Pluggable export backends.

This package is the extension point for shipping analysis results to external
systems. It defines a small :class:`~f1_analysis.exporters.base.Exporter`
contract plus a name-based registry, so new backends (the planned Grafana
export, CSV dumps, a metrics push gateway, ...) can be added without touching
the data or app layers.

Register a backend with the :func:`register` decorator and retrieve it via
:func:`get_exporter`.
"""

# The `grafana` import is a side-effect import: loading it registers the
# built-in backend in the registry.
from f1_analysis.exporters import grafana as _grafana  # noqa: F401
from f1_analysis.exporters.base import Exporter, ExportError, ExportPayload
from f1_analysis.exporters.registry import available, get_exporter, register

__all__ = [
    "Exporter",
    "ExportError",
    "ExportPayload",
    "available",
    "get_exporter",
    "register",
]

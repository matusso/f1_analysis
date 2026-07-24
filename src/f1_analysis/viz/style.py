"""Shared visual language for the pit-wall aesthetic.

Central definition of the colour palette and the Plotly layout used across every
chart, so figures and timing tables read as one system. Timing colours follow
Formula 1 broadcast convention:

* **purple**  — overall (session) fastest
* **green**   — personal best / improvement
* **yellow**  — a set but slower time (baseline)
* **red**     — loss / in-pit / out lap
"""

from __future__ import annotations

from typing import Any

# --- Core surfaces -----------------------------------------------------------
BACKGROUND = "#0a0a0a"
SURFACE = "#12151a"
SURFACE_ALT = "#171b22"
GRID = "#20262f"
BORDER = "#2a313c"
TEXT = "#e8e8e8"
MUTED = "#8a93a2"

# --- Timing semantics --------------------------------------------------------
ACCENT = "#00e5ff"  # cyan — UI accent / current
PURPLE = "#b13bff"  # overall fastest
GREEN = "#00e676"  # personal best / gain
YELLOW = "#ffd400"  # slower / baseline
RED = "#ff2d55"  # loss / pit / out

MONO_STACK = (
    '"JetBrains Mono", "Roboto Mono", "SFMono-Regular", "Consolas", '
    '"Menlo", ui-monospace, monospace'
)


def pitwall_layout(**overrides: Any) -> dict[str, Any]:
    """Return a Plotly ``layout`` dict for the pit-wall look.

    Pass keyword overrides (e.g. ``title="Speed"``) to merge on top.
    """
    layout: dict[str, Any] = {
        "paper_bgcolor": BACKGROUND,
        "plot_bgcolor": BACKGROUND,
        "font": {"family": MONO_STACK, "color": TEXT, "size": 12},
        "margin": {"l": 48, "r": 16, "t": 40, "b": 40},
        "hovermode": "x unified",
        "hoverlabel": {"font": {"family": MONO_STACK}, "bgcolor": SURFACE},
        "legend": {
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "x": 0,
            "font": {"family": MONO_STACK, "size": 11},
        },
        "xaxis": {
            "gridcolor": GRID,
            "zerolinecolor": GRID,
            "linecolor": BORDER,
            "tickfont": {"family": MONO_STACK, "size": 10, "color": MUTED},
        },
        "yaxis": {
            "gridcolor": GRID,
            "zerolinecolor": GRID,
            "linecolor": BORDER,
            "tickfont": {"family": MONO_STACK, "size": 10, "color": MUTED},
        },
    }
    layout.update(overrides)
    return layout

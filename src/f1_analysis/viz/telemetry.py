"""Telemetry chart construction.

Returns interactive Plotly figures. (The previous implementation built
Matplotlib figures and passed them to ``st.plotly_chart``, which does not
render Matplotlib — the charts are now native Plotly and interactive.)
"""

from __future__ import annotations

from dataclasses import dataclass

import plotly.graph_objects as go
from fastf1.core import Lap

from f1_analysis.data.models import DriverRef
from f1_analysis.viz.style import pitwall_layout


@dataclass(frozen=True, slots=True)
class TelemetryChannel:
    """A single comparable telemetry channel."""

    key: str  # column name in FastF1 car data
    title: str
    y_label: str


# The channels the app compares, in display order.
TELEMETRY_CHANNELS: tuple[TelemetryChannel, ...] = (
    TelemetryChannel("Speed", "Speed", "Speed (km/h)"),
    TelemetryChannel("nGear", "Gear", "Gear"),
    TelemetryChannel("RPM", "RPM", "RPM"),
    TelemetryChannel("Throttle", "Throttle", "Throttle (%)"),
    TelemetryChannel("Brake", "Brake", "Brake"),
    TelemetryChannel("DRS", "DRS", "DRS"),
)

_X_LABEL = "Distance (m)"


def compare_channel(
    channel: TelemetryChannel,
    lap_one: Lap,
    driver_one: DriverRef,
    lap_two: Lap,
    driver_two: DriverRef,
) -> go.Figure:
    """Build a distance-domain comparison figure for two drivers' laps."""
    tel_one = lap_one.get_car_data().add_distance()
    tel_two = lap_two.get_car_data().add_distance()

    # Guarantee visually distinct traces when teammates share a colour.
    color_one = driver_one.team_color
    color_two = driver_two.team_color
    if color_one == color_two:
        color_two = "#FFFFFF"

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=tel_one["Distance"],
            y=tel_one[channel.key],
            name=driver_one.abbreviation,
            line={"color": color_one, "width": 2},
            mode="lines",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=tel_two["Distance"],
            y=tel_two[channel.key],
            name=driver_two.abbreviation,
            line={"color": color_two, "width": 2},
            mode="lines",
        )
    )
    figure.update_layout(
        **pitwall_layout(
            xaxis_title=_X_LABEL,
            yaxis_title=channel.y_label,
        )
    )
    return figure

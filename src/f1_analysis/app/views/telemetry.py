"""Telemetry tab: side-by-side channel comparison for two drivers' laps."""

from __future__ import annotations

import streamlit as st
from fastf1.core import Session

from f1_analysis.app.widgets import driver_lap_selector
from f1_analysis.data import build_driver_index
from f1_analysis.data.loader import lap_sectors
from f1_analysis.data.models import DriverRef, LapSectors
from f1_analysis.viz import TELEMETRY_CHANNELS, compare_channel


def _render_sectors(sectors: LapSectors, reference: LapSectors | None = None) -> None:
    """Show sector-time metrics, optionally with a delta to a reference lap."""
    cols = st.columns(3)
    deltas = sectors.delta_to(reference) if reference else (None, None, None)
    values = (sectors.sector1, sectors.sector2, sectors.sector3)
    for col, index, value, delta in zip(cols, range(1, 4), values, deltas, strict=True):
        col.metric(
            f"Sector {index}",
            "—" if value is None else f"{value:.3f}",
            delta=None if delta is None else f"{delta:+.3f}",
            delta_color="inverse",
        )


def render_telemetry(session: Session) -> None:
    laps = session.laps
    driver_index: dict[str, DriverRef] = build_driver_index(session)

    left, right = st.columns(2)
    with left:
        driver_one, lap_one = driver_lap_selector(
            laps, driver_index, label="Select driver #1", key_prefix="tel1"
        )
        sectors_one = lap_sectors(lap_one)
        _render_sectors(sectors_one)

    with right:
        driver_two, lap_two = driver_lap_selector(
            laps, driver_index, label="Select driver #2", key_prefix="tel2"
        )
        _render_sectors(lap_sectors(lap_two), reference=sectors_one)

    for channel in TELEMETRY_CHANNELS:
        st.subheader(channel.title)
        figure = compare_channel(channel, lap_one, driver_one, lap_two, driver_two)
        st.plotly_chart(figure, width="stretch")

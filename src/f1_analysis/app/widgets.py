"""Reusable Streamlit widgets shared across views."""

from __future__ import annotations

import streamlit as st
from fastf1.core import Lap, Laps

from f1_analysis.data import DriverRef
from f1_analysis.data.loader import driver_lap_count, fastest_lap_number, get_lap


def driver_lap_selector(
    laps: Laps,
    driver_index: dict[str, DriverRef],
    *,
    label: str,
    key_prefix: str,
) -> tuple[DriverRef, Lap]:
    """Render a driver picker + lap slider and return the selected driver/lap.

    ``key_prefix`` namespaces the widget keys so the same selector can appear on
    multiple tabs without colliding in Streamlit's session state.
    """
    full_name = st.selectbox(label, list(driver_index), key=f"{key_prefix}_driver")
    driver = driver_index[full_name]

    lap_count = driver_lap_count(laps, driver.abbreviation)
    use_best = st.checkbox("Best lap", key=f"{key_prefix}_best")

    default_lap = fastest_lap_number(laps, driver.abbreviation) if use_best else 1

    lap_number = st.slider(
        "Lap",
        min_value=1,
        max_value=max(lap_count, 1),
        value=default_lap,
        key=f"{key_prefix}_lap",
        disabled=use_best,
    )

    lap = get_lap(laps, driver.abbreviation, lap_number)
    return driver, lap

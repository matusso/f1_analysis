"""Stats tab: inspect the raw lap record for two selected laps."""

from __future__ import annotations

import pandas as pd
import streamlit as st
from fastf1.core import Session

from f1_analysis.app.widgets import driver_lap_selector
from f1_analysis.data import build_driver_index
from f1_analysis.data.models import DriverRef


def render_stats(session: Session) -> None:
    laps = session.laps
    driver_index: dict[str, DriverRef] = build_driver_index(session)

    left, right = st.columns(2)
    with left:
        driver_one, lap_one = driver_lap_selector(
            laps, driver_index, label="Select driver #1", key_prefix="stats1"
        )
    with right:
        driver_two, lap_two = driver_lap_selector(
            laps, driver_index, label="Select driver #2", key_prefix="stats2"
        )

    # Present each lap as a labelled column, transposed for readability.
    frame = pd.DataFrame(
        {driver_one.abbreviation: lap_one, driver_two.abbreviation: lap_two}
    )
    st.dataframe(frame, width="stretch")

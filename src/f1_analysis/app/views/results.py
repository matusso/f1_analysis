"""Results tab: qualifying classification and per-driver Q1/Q2/Q3 times."""

from __future__ import annotations

import pandas as pd
import streamlit as st
from fastf1.core import Session

_QUALI_COLUMNS = ["Position", "FullName", "TeamName", "Q1", "Q2", "Q3"]


def _format_laptime(value: object) -> str:
    """Render a lap time as ``M:SS.mmm``; blank when the driver has no time."""
    delta = pd.to_timedelta(value)
    if pd.isna(delta):
        return ""
    total = delta.total_seconds()
    minutes, seconds = divmod(total, 60)
    return f"{int(minutes)}:{seconds:06.3f}"


def render_results(session: Session) -> None:
    st.subheader("Qualifying results")

    results = session.results.copy()
    display = pd.DataFrame(
        {
            "Pos": results["Position"].astype("Int64"),
            "Driver": results["FullName"],
            "Team": results["TeamName"],
            "Q1": results["Q1"].map(_format_laptime),
            "Q2": results["Q2"].map(_format_laptime),
            "Q3": results["Q3"].map(_format_laptime),
        }
    ).sort_values("Pos")

    st.table(display.set_index("Pos"))

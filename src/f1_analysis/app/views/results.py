"""Results tab: qualifying classification as a pit-wall timing board."""

from __future__ import annotations

import pandas as pd
import streamlit as st
from fastf1.core import Session

from f1_analysis.app.theme import timing_table_html
from f1_analysis.data.loader import normalise_hex

_Q_COLUMNS = ("Q1", "Q2", "Q3")


def _format_laptime(seconds: float) -> str:
    """Render seconds as ``M:SS.mmm``; blank when there is no time."""
    if pd.isna(seconds):
        return "—"
    minutes, secs = divmod(float(seconds), 60)
    return f"{int(minutes)}:{secs:06.3f}"


def render_results(session: Session) -> None:
    st.subheader("Qualifying — best sector & lap times")

    results = session.results.copy()
    results = results.sort_values("Position")

    # Numeric seconds (for heat scaling) keyed by position for a stable index.
    numeric = pd.DataFrame(index=results.index)
    for col in _Q_COLUMNS:
        numeric[col] = pd.to_timedelta(results[col]).dt.total_seconds()

    display = pd.DataFrame(index=results.index)
    display["POS"] = results["Position"].astype("Int64").astype(str)
    display["DRIVER"] = results["Abbreviation"]
    display["TEAM"] = results["TeamName"]
    for col in _Q_COLUMNS:
        display[col] = numeric[col].map(_format_laptime)

    # Align numeric frame to the display columns so styling lookups line up.
    numeric = numeric.reindex(columns=list(display.columns), fill_value=float("nan"))

    team_colors = {
        idx: normalise_hex(color) for idx, color in results["TeamColor"].items()
    }

    html = timing_table_html(
        numeric=numeric,
        display=display,
        heat_columns=list(_Q_COLUMNS),
        team_colors=team_colors,
        text_columns=["DRIVER", "TEAM"],
    )
    st.markdown(html, unsafe_allow_html=True)

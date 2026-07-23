"""Streamlit application entry point.

Run with either::

    streamlit run streamlit_app.py          # repo-root launcher
    streamlit run src/f1_analysis/app/main.py

Both require the package to be importable (``pip install -e .``).
"""

from __future__ import annotations

import streamlit as st

from f1_analysis.app.views import render_results, render_stats, render_telemetry
from f1_analysis.config import get_settings
from f1_analysis.data import list_event_locations, load_session

_SESSIONS = ("Practice 1", "Practice 2", "Practice 3", "Qualifying", "Race")


def _sidebar() -> tuple[int, str, str]:
    """Render the sidebar selectors and return (year, circuit, session)."""
    settings = get_settings()
    with st.sidebar:
        year = st.selectbox("Season", settings.available_years, index=0)
        locations = list_event_locations(year)
        circuit = st.selectbox("Circuit", locations)
        session_name = st.selectbox("Session", _SESSIONS)
    return year, circuit, session_name


def main() -> None:
    settings = get_settings()
    st.set_page_config(page_title=f"{settings.app_title} (by matusso)", layout="wide")

    year, circuit, session_name = _sidebar()
    st.header(f"{year} — {circuit}")

    telemetry_tab, stats_tab, results_tab = st.tabs(["Telemetry", "Stats", "Results"])

    with telemetry_tab:
        render_telemetry(load_session(year, circuit, session_name))

    with stats_tab:
        render_stats(load_session(year, circuit, session_name))

    with results_tab:
        render_results(load_session(year, circuit, "Q"))


if __name__ == "__main__":
    main()

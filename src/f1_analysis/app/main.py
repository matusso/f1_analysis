"""Streamlit application entry point.

Run with either::

    streamlit run streamlit_app.py          # repo-root launcher
    streamlit run src/f1_analysis/app/main.py

Both require the package to be importable (``pip install -e .``).
"""

from __future__ import annotations

import streamlit as st

from f1_analysis.app.theme import inject_css, render_badge
from f1_analysis.app.views import render_results, render_stats, render_telemetry
from f1_analysis.config import get_settings
from f1_analysis.data import list_event_locations, load_session

_SESSIONS = ("Practice 1", "Practice 2", "Practice 3", "Qualifying", "Race")
_DASHBOARDS = ("Telemetry", "Stats", "Results")


def _control_bar() -> tuple[int, str, str, str]:
    """Render the status bar — its segments are live dropdowns.

    Returns the selected (year, circuit, session, dashboard).
    """
    settings = get_settings()
    with st.container(key="pw-controls"):
        season_col, circuit_col, session_col, dashboard_col, _spacer, badge_col = st.columns(
            [1.6, 2.0, 2.2, 2.2, 1.8, 1.9], vertical_alignment="center"
        )
        with season_col:
            year = st.selectbox("Season", settings.available_years, index=0)
        with circuit_col:
            circuit = st.selectbox("Circuit", list_event_locations(year))
        with session_col:
            session_name = st.selectbox("Session", _SESSIONS)
        with dashboard_col:
            dashboard = st.selectbox("Dashboard", _DASHBOARDS)
        with badge_col:
            render_badge("Data Loaded")
    return year, circuit, session_name, dashboard


def main() -> None:
    settings = get_settings()
    st.set_page_config(
        page_title=f"{settings.app_title} (by matusso)",
        page_icon="🏁",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    inject_css()

    year, circuit, session_name, dashboard = _control_bar()

    # Only the selected dashboard's session is loaded.
    if dashboard == "Telemetry":
        render_telemetry(load_session(year, circuit, session_name))
    elif dashboard == "Stats":
        render_stats(load_session(year, circuit, session_name))
    else:  # Results — always the qualifying classification
        render_results(load_session(year, circuit, "Q"))


if __name__ == "__main__":
    main()

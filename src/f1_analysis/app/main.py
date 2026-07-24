"""Streamlit application entry point.

Run with either::

    streamlit run streamlit_app.py          # repo-root launcher
    streamlit run src/f1_analysis/app/main.py

Both require the package to be importable (``pip install -e .``).
"""

from __future__ import annotations

from collections.abc import Callable

import streamlit as st
from fastf1.core import Session
from fastf1.exceptions import DataNotLoadedError

from f1_analysis.app.theme import inject_css, render_badge, render_unavailable
from f1_analysis.app.views import render_results, render_telemetry
from f1_analysis.config import get_settings
from f1_analysis.data import list_event_locations, load_session

_SESSIONS = ("Practice 1", "Practice 2", "Practice 3", "Qualifying", "Race")
_DASHBOARDS = ("Telemetry", "Results")


def _is_empty(getter: Callable[[], object]) -> bool:
    """True if a FastF1 data accessor is empty or was never loaded."""
    try:
        return bool(getter().empty)  # type: ignore[attr-defined]
    except DataNotLoadedError:
        return True


@st.cache_resource(show_spinner="Loading session data…")
def _cached_session(year: int, circuit: str, session_name: str, telemetry: bool) -> Session:
    """Load a session once per (selection, telemetry) and reuse across reruns.

    Caching avoids re-hitting the FastF1 data API on every widget interaction.
    If the fetch produced no data at all (API unreachable, or a future session),
    we raise instead of returning — Streamlit does not cache on exception, so the
    next interaction retries rather than caching an empty session.
    """
    session = load_session(year, circuit, session_name, telemetry=telemetry, weather=False)
    if _is_empty(lambda: session.laps) and _is_empty(lambda: session.results):
        raise DataNotLoadedError(f"No data loaded for {circuit} {session_name}.")
    return session


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

    # Only the selected dashboard's session is loaded (telemetry only when needed).
    try:
        session = _cached_session(
            year, circuit, session_name, telemetry=(dashboard == "Telemetry")
        )
        if dashboard == "Telemetry":
            render_telemetry(session)
        else:  # Results — classification for the chosen session
            render_results(session)
    except DataNotLoadedError:
        render_unavailable(
            f"Timing data for <b>{circuit} · {session_name}</b> could not be loaded. "
            "The session may not have taken place yet, or the F1 data provider is "
            "temporarily unavailable — try another session or season."
        )


if __name__ == "__main__":
    main()

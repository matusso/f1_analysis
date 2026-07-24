"""Results tab: session classification as a pit-wall timing board.

Adapts to the selected session:

* **Practice** — fastest-lap leaderboard (best lap + gap + laps run).
* **Qualifying / Sprint Shootout** — Q1/Q2/Q3 with fastest-time heat colours.
* **Race / Sprint** — finishing classification (grid, gap, points, status).
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
from fastf1.core import Session

from f1_analysis.app.theme import render_unavailable, timing_table_html
from f1_analysis.data.loader import normalise_hex

_Q_COLUMNS = ("Q1", "Q2", "Q3")
_QUALI_SESSIONS = {"Qualifying", "Sprint Qualifying", "Sprint Shootout"}


# --------------------------------------------------------------------------- #
# Formatting helpers
# --------------------------------------------------------------------------- #
def _fmt_laptime(seconds: float | None) -> str:
    if seconds is None or pd.isna(seconds):
        return "—"
    minutes, secs = divmod(float(seconds), 60)
    return f"{int(minutes)}:{secs:06.3f}"


def _fmt_gap(seconds: float) -> str:
    if seconds < 60:
        return f"+{seconds:.3f}"
    minutes, secs = divmod(seconds, 60)
    return f"+{int(minutes)}:{secs:06.3f}"


def _fmt_total_time(seconds: float) -> str:
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{int(hours)}:{int(minutes):02d}:{secs:06.3f}"
    return f"{int(minutes)}:{secs:06.3f}"


def _fmt_int(series: pd.Series) -> list[str]:
    """Nullable-int column to strings, blanking missing values."""
    return ["—" if pd.isna(v) else str(int(v)) for v in series]


def _driver_meta(session: Session) -> dict[str, tuple[str, str, str]]:
    """Map abbreviation -> (full name, team name, normalised team colour)."""
    meta: dict[str, tuple[str, str, str]] = {}
    for _, row in session.results.iterrows():
        meta[row["Abbreviation"]] = (
            row["FullName"],
            row.get("TeamName", "") or "",
            normalise_hex(row.get("TeamColor")),
        )
    return meta


def _emit(
    numeric: pd.DataFrame,
    display: pd.DataFrame,
    heat_columns: list[str],
    team_colors: dict[int, str],
) -> None:
    numeric = numeric.reindex(columns=list(display.columns), fill_value=float("nan"))
    html = timing_table_html(
        numeric=numeric,
        display=display,
        heat_columns=heat_columns,
        team_colors=team_colors,
        text_columns=["DRIVER", "TEAM", "STATUS"],
    )
    st.markdown(html, unsafe_allow_html=True)


# --------------------------------------------------------------------------- #
# Per-session boards
# --------------------------------------------------------------------------- #
def _render_qualifying(session: Session) -> None:
    st.subheader(f"{session.name} — best sector & lap times")
    if session.results.empty:
        render_unavailable("No qualifying classification is available for this session.")
        return
    results = session.results.copy().sort_values("Position").reset_index(drop=True)

    numeric = pd.DataFrame(index=results.index)
    display = pd.DataFrame(index=results.index)
    display["POS"] = _fmt_int(results["Position"])
    display["DRIVER"] = results["Abbreviation"]
    display["TEAM"] = results["TeamName"]
    for col in _Q_COLUMNS:
        numeric[col] = pd.to_timedelta(results[col]).dt.total_seconds()
        display[col] = numeric[col].map(_fmt_laptime)

    team_colors = {i: normalise_hex(c) for i, c in results["TeamColor"].items()}
    _emit(numeric, display, list(_Q_COLUMNS), team_colors)


def _render_race(session: Session) -> None:
    st.subheader(f"{session.name} — classification")
    if session.results.empty:
        render_unavailable("No classification is available for this session yet.")
        return
    results = session.results.copy().sort_values("Position").reset_index(drop=True)

    times = pd.to_timedelta(results["Time"]).dt.total_seconds()

    def gap_cell(i: int) -> str:
        value = times.iloc[i]
        if pd.isna(value):
            return "—"
        return _fmt_total_time(value) if i == 0 else _fmt_gap(value)

    display = pd.DataFrame(index=results.index)
    display["POS"] = _fmt_int(results["Position"])
    display["DRIVER"] = results["Abbreviation"]
    display["TEAM"] = results["TeamName"]
    display["GRID"] = _fmt_int(results["GridPosition"])
    display["GAP/TIME"] = [gap_cell(i) for i in results.index]
    display["PTS"] = results["Points"].fillna(0).astype(int).astype(str)
    display["STATUS"] = results["Status"].fillna("")

    team_colors = {i: normalise_hex(c) for i, c in results["TeamColor"].items()}
    _emit(pd.DataFrame(index=results.index), display, [], team_colors)


def _render_practice(session: Session) -> None:
    st.subheader(f"{session.name} — fastest laps")
    meta = _driver_meta(session)
    laps = session.laps

    rows: list[tuple[str, float, int]] = []
    for abbreviation in laps["Driver"].unique():
        driver_laps = laps.pick_drivers(abbreviation)
        fastest = driver_laps.pick_fastest()
        if fastest is None:
            continue
        seconds = pd.to_timedelta(fastest["LapTime"]).total_seconds()
        if pd.isna(seconds):
            continue
        rows.append((abbreviation, float(seconds), len(driver_laps)))

    if not rows:
        st.info("No timed laps available for this session yet.")
        return

    rows.sort(key=lambda item: item[1])
    best = rows[0][1]

    index = list(range(len(rows)))
    numeric = pd.DataFrame({"BEST": [r[1] for r in rows]}, index=index)
    display = pd.DataFrame(index=index)
    display["POS"] = [str(i + 1) for i in index]
    display["DRIVER"] = [rows[i][0] for i in index]
    display["TEAM"] = [meta.get(rows[i][0], ("", "", ""))[1] for i in index]
    display["BEST"] = [_fmt_laptime(r[1]) for r in rows]
    display["GAP"] = ["—" if i == 0 else _fmt_gap(rows[i][1] - best) for i in index]
    display["LAPS"] = [str(r[2]) for r in rows]

    team_colors = {i: meta.get(rows[i][0], ("", "", "#FFFFFF"))[2] for i in index}
    _emit(numeric, display, ["BEST"], team_colors)


def render_results(session: Session) -> None:
    name = session.name
    if "Practice" in name:
        _render_practice(session)
    elif name in _QUALI_SESSIONS:
        _render_qualifying(session)
    else:  # Race, Sprint
        _render_race(session)

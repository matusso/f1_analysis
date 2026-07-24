"""Pit-wall visual theme for the Streamlit app.

Everything here is presentation-only: a global CSS injection, a status-bar
header component, and helpers to render timing tables with Formula 1 broadcast
heat colours. Colours are sourced from :mod:`f1_analysis.viz.style` so charts
and tables stay visually consistent.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from f1_analysis.viz import style as S

# ---------------------------------------------------------------------------
# Global CSS
# ---------------------------------------------------------------------------

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {{
    --pw-bg: {S.BACKGROUND};
    --pw-surface: {S.SURFACE};
    --pw-surface-alt: {S.SURFACE_ALT};
    --pw-border: {S.BORDER};
    --pw-text: {S.TEXT};
    --pw-muted: {S.MUTED};
    --pw-accent: {S.ACCENT};
    --pw-purple: {S.PURPLE};
    --pw-green: {S.GREEN};
    --pw-yellow: {S.YELLOW};
    --pw-red: {S.RED};
}}

html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"] {{
    font-family: {S.MONO_STACK};
    background-color: var(--pw-bg);
}}

/* Tighten the layout so the board reads dense, like a real timing screen. */
.block-container {{ padding-top: 1.4rem; padding-bottom: 2rem; max-width: 100%; }}
[data-testid="stHeader"] {{ background: transparent; }}

/* Headings: condensed, upper-case, cyan accent. */
h1, h2, h3, h4 {{
    font-family: {S.MONO_STACK};
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--pw-text);
    font-weight: 700;
}}
h2, h3 {{
    border-left: 3px solid var(--pw-accent);
    padding-left: 0.55rem;
    color: var(--pw-accent);
    font-size: 1.0rem !important;
}}

/* Sidebar removed — controls live in the status bar. */
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {{ display: none !important; }}

/* In-tab dropdowns (driver pickers) */
[data-testid="stSelectbox"] label {{
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-size: 0.68rem;
    color: var(--pw-muted);
}}
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
    background-color: var(--pw-surface);
    border: 1px solid var(--pw-border);
    border-radius: 3px;
    font-family: {S.MONO_STACK};
    font-weight: 600;
}}
[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {{
    border-color: var(--pw-accent);
}}

/* ---- Status bar: segments are live dropdowns ---------------------------
   The whole row is framed as one bar; each segment column carries a right
   divider, a tiny upper-case label, and a large monospace value. */
.st-key-pw-controls [data-testid="stHorizontalBlock"] {{
    border: 1px solid var(--pw-border);
    background: var(--pw-surface);
    border-radius: 4px;
    gap: 0;
    margin-bottom: 1.1rem;
    align-items: stretch;
}}
.st-key-pw-controls [data-testid="stColumn"]:nth-child(-n+4) {{
    border-right: 1px solid var(--pw-border);
}}
.st-key-pw-controls [data-testid="stColumn"] {{ padding: 0.4rem 0.85rem; }}

/* Tiny segment label */
.st-key-pw-controls [data-testid="stSelectbox"] label {{
    margin-bottom: 0.05rem;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    color: var(--pw-muted);
}}
/* Turn the select into a borderless, large-value readout */
.st-key-pw-controls [data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
    background: transparent;
    border: none;
    box-shadow: none;
    padding-left: 0;
    min-height: 2rem;
}}
.st-key-pw-controls [data-testid="stSelectbox"] div[data-baseweb="select"],
.st-key-pw-controls [data-testid="stSelectbox"] div[data-baseweb="select"] * {{
    font-family: {S.MONO_STACK};
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--pw-text) !important;
}}
/* Keep the value fully visible and shrink the chevron footprint. */
.st-key-pw-controls [data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child {{
    overflow: visible;
}}
.st-key-pw-controls [data-testid="stSelectbox"] svg {{
    height: 0.95rem !important;
    width: 0.95rem !important;
}}
/* First segment (Season) picks up the cyan accent, like the reference. */
.st-key-pw-controls [data-testid="stColumn"]:first-child div[data-baseweb="select"],
.st-key-pw-controls [data-testid="stColumn"]:first-child div[data-baseweb="select"] * {{
    color: var(--pw-accent) !important;
}}
/* Badge sits flush right in its column */
.st-key-pw-controls [data-testid="stColumn"]:last-child {{
    display: flex; justify-content: flex-end; align-items: center;
    border-right: none;
}}
.st-key-pw-controls .pw-badge {{ margin: 0; }}

/* Tabs */
[data-baseweb="tab-list"] {{ gap: 2px; border-bottom: 1px solid var(--pw-border); }}
[data-baseweb="tab"] {{
    background-color: var(--pw-surface);
    border: 1px solid var(--pw-border);
    border-bottom: none;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-size: 0.8rem;
    padding: 0.35rem 1.1rem;
}}
[data-baseweb="tab"][aria-selected="true"] {{
    color: var(--pw-bg);
    background-color: var(--pw-accent);
    font-weight: 700;
}}

/* Metrics -> compact instrument tiles */
[data-testid="stMetric"] {{
    background-color: var(--pw-surface);
    border: 1px solid var(--pw-border);
    border-radius: 3px;
    padding: 0.5rem 0.7rem;
}}
[data-testid="stMetricLabel"] {{
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--pw-muted);
    font-size: 0.7rem;
}}
[data-testid="stMetricValue"] {{
    font-family: {S.MONO_STACK};
    font-weight: 700;
    font-size: 1.35rem;
    color: var(--pw-text);
}}

/* ---- Status badge ------------------------------------------------------ */
.pw-badge {{
    display: inline-block; padding: 0.28rem 0.8rem;
    border-radius: 3px; font-weight: 700; font-size: 0.75rem;
    letter-spacing: 0.1em; text-transform: uppercase;
    background: rgba(0,230,118,0.14); color: var(--pw-green);
    border: 1px solid var(--pw-green);
}}

/* ---- Timing table ------------------------------------------------------ */
.pw-timing {{ border-collapse: collapse; width: 100%; font-family: {S.MONO_STACK}; }}
.pw-timing th {{
    background: var(--pw-surface-alt); color: var(--pw-muted);
    text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.68rem;
    text-align: right; padding: 0.4rem 0.6rem; border-bottom: 1px solid var(--pw-border);
}}
.pw-timing td {{
    padding: 0.28rem 0.6rem; font-size: 0.82rem; text-align: right;
    border-bottom: 1px solid #14181e; white-space: nowrap;
}}
.pw-timing td.txt {{ text-align: left; }}
</style>
"""


def inject_css() -> None:
    """Inject the global pit-wall stylesheet (call once, early)."""
    st.markdown(_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Status bar
# ---------------------------------------------------------------------------


def render_badge(text: str) -> None:
    """Render the status badge shown at the right of the control bar."""
    st.markdown(f'<div class="pw-badge">{text}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Timing-table heat colouring
# ---------------------------------------------------------------------------


def _lerp_hex(a: str, b: str, t: float) -> str:
    t = max(0.0, min(1.0, t))
    ar, ag, ab = (int(a[i : i + 2], 16) for i in (1, 3, 5))
    br, bg, bb = (int(b[i : i + 2], 16) for i in (1, 3, 5))
    r = round(ar + (br - ar) * t)
    g = round(ag + (bg - ag) * t)
    bl = round(ab + (bb - ab) * t)
    return f"#{r:02x}{g:02x}{bl:02x}"


def _heat(t: float) -> str:
    """Green (fast) -> yellow -> red (slow) for a normalised gap ``t``."""
    if t <= 0.5:
        return _lerp_hex(S.GREEN, S.YELLOW, t / 0.5)
    return _lerp_hex(S.YELLOW, S.RED, (t - 0.5) / 0.5)


def _cell_css(bg: str, dark_text: bool = True) -> str:
    fg = "#0a0a0a" if dark_text else "#ffffff"
    return f"background-color:{bg};color:{fg};font-weight:600;"


def timing_table_html(
    numeric: pd.DataFrame,
    display: pd.DataFrame,
    heat_columns: list[str],
    team_colors: dict[int, str],
    text_columns: list[str],
) -> str:
    """Build a heat-coloured timing table as standalone HTML.

    Args:
        numeric: numeric values (seconds) used only for colour scaling.
        display: pre-formatted strings shown in each cell.
        heat_columns: columns to colour green->red, min highlighted purple.
        team_colors: row-index -> team colour (used to tint the first text col).
        text_columns: left-aligned, non-numeric columns.
    """
    styles = pd.DataFrame("", index=display.index, columns=display.columns)

    for col in heat_columns:
        values = numeric[col]
        finite = values.dropna()
        if finite.empty:
            continue
        fastest = finite.min()
        spread = finite.max() - fastest
        for idx, value in values.items():
            if pd.isna(value):
                continue
            if value == fastest:
                styles.at[idx, col] = _cell_css(S.PURPLE, dark_text=False)
            else:
                t = 0.0 if spread == 0 else (value - fastest) / spread
                styles.at[idx, col] = _cell_css(_heat(t), dark_text=True)

    # Tint the leading text column (driver) with the team colour.
    if text_columns:
        driver_col = text_columns[0]
        for idx in display.index:
            color = team_colors.get(idx)
            if color:
                styles.at[idx, driver_col] = f"color:{color};font-weight:700;"

    header = "".join(f"<th>{c}</th>" for c in display.columns)
    rows = []
    for idx in display.index:
        cells = []
        for col in display.columns:
            css = styles.at[idx, col]
            klass = ' class="txt"' if col in text_columns else ""
            cells.append(f'<td{klass} style="{css}">{display.at[idx, col]}</td>')
        rows.append(f"<tr>{''.join(cells)}</tr>")
    return (
        f'<table class="pw-timing"><thead><tr>{header}</tr></thead>'
        f"<tbody>{''.join(rows)}</tbody></table>"
    )

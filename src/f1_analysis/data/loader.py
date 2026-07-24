"""FastF1 session access.

Every FastF1 touchpoint lives here so the rest of the app depends on plain
Python types and a small, stable surface — not on FastF1's evolving API. This
module targets FastF1 >= 3.8 (``pick_drivers``, ``Session.load``, ``event``).
"""

from __future__ import annotations

import logging
from functools import lru_cache

import fastf1
import pandas as pd
from fastf1.core import Lap, Laps, Session

from f1_analysis.config import get_settings
from f1_analysis.data.models import DriverRef, LapSectors, LapSummary

logger = logging.getLogger(__name__)

_cache_configured = False


def configure_cache() -> None:
    """Enable FastF1's on-disk cache (idempotent)."""
    global _cache_configured
    if _cache_configured:
        return
    cache_dir = get_settings().ensure_cache_dir()
    fastf1.Cache.enable_cache(str(cache_dir))
    logger.info("FastF1 cache enabled at %s", cache_dir)
    _cache_configured = True


@lru_cache(maxsize=32)
def list_event_locations(year: int) -> tuple[str, ...]:
    """Return the round locations for a season, in schedule order."""
    schedule = fastf1.get_event_schedule(year)
    rounds = schedule[schedule["RoundNumber"] > 0]
    return tuple(rounds["Location"].tolist())


def load_session(
    year: int,
    circuit: str,
    session_name: str,
    *,
    laps: bool = True,
    telemetry: bool = True,
    weather: bool = True,
) -> Session:
    """Load a session with the requested data payloads."""
    configure_cache()
    session = fastf1.get_session(year, circuit, session_name)
    session.load(laps=laps, telemetry=telemetry, weather=weather)
    return session


def normalise_hex(color: str | None) -> str:
    """Return a ``#RRGGBB`` string; fall back to white for missing colours."""
    if not color:
        return "#FFFFFF"
    color = color.strip()
    return color if color.startswith("#") else f"#{color}"


def build_driver_index(session: Session) -> dict[str, DriverRef]:
    """Map each driver's full name to a :class:`DriverRef` for the session."""
    index: dict[str, DriverRef] = {}
    for driver_number in session.drivers:
        info = session.get_driver(driver_number)
        ref = DriverRef(
            full_name=info["FullName"],
            abbreviation=info["Abbreviation"],
            team_name=info.get("TeamName", ""),
            team_color=normalise_hex(info.get("TeamColor")),
        )
        index[ref.full_name] = ref
    return index


def driver_lap_count(laps: Laps, abbreviation: str) -> int:
    """Number of laps recorded for a driver."""
    return len(laps.pick_drivers(abbreviation))


def fastest_lap_number(laps: Laps, abbreviation: str) -> int:
    """1-based lap number of a driver's fastest lap."""
    return int(laps.pick_drivers(abbreviation).pick_fastest()["LapNumber"])


def get_lap(laps: Laps, abbreviation: str, lap_number: int) -> Lap:
    """Return a specific lap for a driver by 1-based lap number."""
    driver_laps = laps.pick_drivers(abbreviation)
    match = driver_laps[driver_laps["LapNumber"] == lap_number]
    if match.empty:
        raise ValueError(f"No lap {lap_number} for driver {abbreviation}")
    return match.iloc[0]


def lap_sectors(lap: Lap) -> LapSectors:
    """Extract sector times (seconds) from a lap, tolerating missing values."""

    def _seconds(value: object) -> float | None:
        seconds = pd.to_timedelta(value).total_seconds()
        return None if pd.isna(seconds) else float(seconds)

    return LapSectors(
        sector1=_seconds(lap["Sector1Time"]),
        sector2=_seconds(lap["Sector2Time"]),
        sector3=_seconds(lap["Sector3Time"]),
    )


def lap_summary(lap: Lap) -> LapSummary:
    """Extract headline lap facts (time, tyre, speed trap), tolerating gaps."""

    def _float(value: object) -> float | None:
        number = pd.to_numeric(value, errors="coerce")
        return None if pd.isna(number) else float(number)

    def _int(value: object) -> int | None:
        number = _float(value)
        return None if number is None else int(number)

    def _bool(value: object) -> bool | None:
        return None if pd.isna(value) else bool(value)

    def _str(value: object) -> str | None:
        return None if pd.isna(value) else str(value)

    lap_time = pd.to_timedelta(lap.get("LapTime")).total_seconds()
    return LapSummary(
        lap_time=None if pd.isna(lap_time) else float(lap_time),
        compound=_str(lap.get("Compound")),
        tyre_life=_int(lap.get("TyreLife")),
        fresh_tyre=_bool(lap.get("FreshTyre")),
        stint=_int(lap.get("Stint")),
        speed_trap=_float(lap.get("SpeedST")),
        is_personal_best=_bool(lap.get("IsPersonalBest")),
    )

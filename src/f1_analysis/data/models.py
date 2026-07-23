"""Typed domain models shared across the data, viz, and app layers.

These deliberately decouple the rest of the codebase from FastF1's pandas
row/Series shapes, which keeps view and exporter code readable and testable.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DriverRef:
    """A driver within a specific session."""

    full_name: str
    abbreviation: str
    team_name: str
    team_color: str  # normalised "#RRGGBB"

    @property
    def label(self) -> str:
        return f"{self.full_name} ({self.abbreviation})"


@dataclass(frozen=True, slots=True)
class LapSectors:
    """Sector times for a single lap, in seconds (``None`` when unavailable)."""

    sector1: float | None
    sector2: float | None
    sector3: float | None

    def delta_to(self, other: LapSectors) -> tuple[float | None, float | None, float | None]:
        """Return ``self - other`` per sector, rounded to milliseconds."""

        def _delta(a: float | None, b: float | None) -> float | None:
            if a is None or b is None:
                return None
            return round(a - b, 3)

        return (
            _delta(self.sector1, other.sector1),
            _delta(self.sector2, other.sector2),
            _delta(self.sector3, other.sector3),
        )

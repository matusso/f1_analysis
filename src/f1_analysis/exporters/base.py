"""Exporter contract shared by all backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class ExportError(RuntimeError):
    """Raised when an export operation fails."""


@dataclass(frozen=True, slots=True)
class ExportPayload:
    """A backend-agnostic bundle of data to export.

    Attributes:
        name: Logical name for the dataset (e.g. ``"2024-monza-qualifying"``).
        rows: Tabular records, one dict per row.
        metadata: Optional context (season, circuit, session, units, ...).
    """

    name: str
    rows: list[dict[str, Any]]
    metadata: dict[str, Any] = field(default_factory=dict)


class Exporter(ABC):
    """Base class for all export backends.

    Subclasses implement :meth:`export`. Keep backends stateless where possible
    and pass configuration in via ``__init__`` so they stay easy to test.
    """

    #: Stable identifier used by the registry and any UI selector.
    name: str = "exporter"

    @abstractmethod
    def export(self, payload: ExportPayload) -> None:
        """Send ``payload`` to the backing system.

        Raises:
            ExportError: If the export cannot be completed.
        """
        raise NotImplementedError

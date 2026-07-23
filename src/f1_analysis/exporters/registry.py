"""Name-based registry for export backends."""

from __future__ import annotations

from collections.abc import Callable

from f1_analysis.exporters.base import Exporter

_REGISTRY: dict[str, type[Exporter]] = {}


def register(cls: type[Exporter]) -> type[Exporter]:
    """Class decorator that registers an :class:`Exporter` by its ``name``."""
    key = cls.name
    if key in _REGISTRY:
        raise ValueError(f"Exporter '{key}' is already registered")
    _REGISTRY[key] = cls
    return cls


def available() -> tuple[str, ...]:
    """Return the names of all registered exporters, sorted."""
    return tuple(sorted(_REGISTRY))


def get_exporter(name: str, **kwargs: object) -> Exporter:
    """Instantiate a registered exporter by name.

    Extra keyword arguments are forwarded to the backend constructor.
    """
    try:
        cls = _REGISTRY[name]
    except KeyError:
        known = ", ".join(available()) or "<none>"
        raise KeyError(f"Unknown exporter '{name}'. Registered: {known}") from None
    return cls(**kwargs)


# Convenience alias mirroring the decorator use-site type.
Factory = Callable[..., Exporter]

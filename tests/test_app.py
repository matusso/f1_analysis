"""Tests for app-level guards."""

from fastf1.exceptions import DataNotLoadedError

from f1_analysis.app.main import _is_empty


class _Frame:
    def __init__(self, empty: bool) -> None:
        self.empty = empty


def test_is_empty_true_for_empty_frame():
    assert _is_empty(lambda: _Frame(empty=True)) is True


def test_is_empty_false_for_populated_frame():
    assert _is_empty(lambda: _Frame(empty=False)) is False


def test_is_empty_true_when_data_not_loaded():
    def boom() -> object:
        raise DataNotLoadedError("not loaded")

    assert _is_empty(boom) is True

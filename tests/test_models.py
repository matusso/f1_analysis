"""Tests for domain models."""

from f1_analysis.data.models import DriverRef, LapSectors


def test_driver_label():
    driver = DriverRef(
        full_name="Charles Leclerc",
        abbreviation="LEC",
        team_name="Ferrari",
        team_color="#DC0000",
    )
    assert driver.label == "Charles Leclerc (LEC)"


def test_sector_delta():
    fast = LapSectors(28.1, 30.2, 22.0)
    slow = LapSectors(28.4, 30.0, 22.5)
    d1, d2, d3 = slow.delta_to(fast)
    assert d1 == 0.3
    assert d2 == -0.2
    assert d3 == 0.5


def test_sector_delta_with_missing():
    a = LapSectors(28.1, None, 22.0)
    b = LapSectors(28.0, 30.0, None)
    assert a.delta_to(b) == (round(0.1, 3), None, None)

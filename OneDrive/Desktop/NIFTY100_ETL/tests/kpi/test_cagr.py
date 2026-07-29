import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.analytics.cagr import calculate_cagr


def test_positive_growth():
    assert calculate_cagr(100, 200, 5) == 14.87


def test_no_growth():
    assert calculate_cagr(100, 100, 5) == 0.0


def test_invalid_begin():
    assert calculate_cagr(0, 100, 5) is None


def test_invalid_end():
    assert calculate_cagr(100, 0, 5) is None


def test_invalid_years():
    assert calculate_cagr(100, 200, 0) is None
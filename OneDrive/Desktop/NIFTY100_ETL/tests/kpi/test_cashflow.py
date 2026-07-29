import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.analytics.cashflow_kpis import *


def test_operating_cashflow_ratio():
    assert operating_cashflow_ratio(100, 50) == 2.0


def test_investment_ratio():
    assert investment_ratio(-50, 100) == 0.5


def test_financing_ratio():
    assert financing_ratio(-20, 100) == 0.2


def test_net_cashflow_margin():
    assert net_cashflow_margin(20, 100) == 20.0


def test_positive_cashflow():
    assert is_positive_cashflow(10) is True


def test_negative_cashflow():
    assert is_positive_cashflow(-10) is False


def test_zero_operating():
    assert investment_ratio(-20, 0) is None


def test_zero_netcash():
    assert operating_cashflow_ratio(100, 0) is None
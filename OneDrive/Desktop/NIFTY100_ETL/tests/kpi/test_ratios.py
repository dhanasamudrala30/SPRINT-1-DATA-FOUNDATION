import sys
from pathlib import Path

# Add project root
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    check_opm,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    is_high_leverage,
    interest_coverage,
    is_debt_free,
    net_debt,
    asset_turnover,
)




def test_net_profit_margin():
    assert net_profit_margin(100, 1000) == 10.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin():
    assert operating_profit_margin(200, 1000) == 20.0


def test_check_opm():
    assert check_opm(20, 18) is True


def test_check_opm_ok():
    assert check_opm(20, 20.5) is False


def test_roe():
    assert return_on_equity(100, 200, 300) == 20.0


def test_roe_negative_equity():
    assert return_on_equity(100, -500, 100) is None


def test_roa():
    assert return_on_assets(100, 1000) == 10.0




def test_debt_to_equity():
    assert debt_to_equity(500, 200, 300) == 1.0


def test_debt_to_equity_zero_equity():
    assert debt_to_equity(500, -200, 100) is None


def test_high_leverage():
    assert is_high_leverage(2.5) is True


def test_normal_leverage():
    assert is_high_leverage(1.2) is False


def test_interest_coverage():
    assert interest_coverage(200, 20) == 10.0


def test_debt_free():
    assert is_debt_free(0) is True


def test_net_debt():
    assert net_debt(500, 150) == 350


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2.0
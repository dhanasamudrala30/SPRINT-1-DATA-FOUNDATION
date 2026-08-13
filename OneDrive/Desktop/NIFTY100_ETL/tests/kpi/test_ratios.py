import pytest

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


# ============================================================
# DAY 41 — KPI / RATIOS UNIT TESTS
# ============================================================


# ------------------------------------------------------------
# Net Profit Margin
# ------------------------------------------------------------

def test_net_profit_margin_normal():
    assert net_profit_margin(200, 1000) == 20.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(200, 0) is None


# ------------------------------------------------------------
# Operating Profit Margin
# ------------------------------------------------------------

def test_operating_profit_margin_normal():
    assert operating_profit_margin(300, 1000) == 30.0


def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(300, 0) is None


# ------------------------------------------------------------
# OPM Cross-check
# ------------------------------------------------------------

def test_opm_divergence_flag():
    assert check_opm(20, 25) is True


def test_opm_no_divergence():
    assert check_opm(20, 20.5) is False


# ------------------------------------------------------------
# ROE
# ------------------------------------------------------------

def test_roe_positive_equity():
    assert return_on_equity(
        100,
        400,
        600,
    ) == 10.0


def test_roe_negative_equity_returns_none():
    assert return_on_equity(
        100,
        -500,
        200,
    ) is None


# ------------------------------------------------------------
# ROCE
# ------------------------------------------------------------

def test_roce_positive_capital():
    result = return_on_capital_employed(
        operating_profit=200,
        other_income=20,
        depreciation=20,
        equity_capital=500,
        reserves=500,
        borrowings=100,
    )

    assert result == 18.18


def test_roce_negative_capital_returns_none():
    result = return_on_capital_employed(
        operating_profit=100,
        other_income=0,
        depreciation=10,
        equity_capital=-1000,
        reserves=0,
        borrowings=0,
    )

    assert result is None


# ------------------------------------------------------------
# ROA
# ------------------------------------------------------------

def test_roa_normal():
    assert return_on_assets(100, 1000) == 10.0


def test_roa_zero_assets():
    assert return_on_assets(100, 0) is None


# ------------------------------------------------------------
# Debt to Equity
# ------------------------------------------------------------

def test_debt_to_equity_normal():
    assert debt_to_equity(
        200,
        500,
        500,
    ) == 0.2


def test_debt_to_equity_negative_equity():
    assert debt_to_equity(
        200,
        -700,
        100,
    ) is None


# ------------------------------------------------------------
# High Leverage
# ------------------------------------------------------------

def test_high_leverage_above_default_threshold():
    assert is_high_leverage(3.0) is True


def test_normal_leverage():
    assert is_high_leverage(1.5) is False


def test_debt_to_equity_above_5_threshold():
    assert is_high_leverage(
        5.5,
        threshold=5.0,
    ) is True


# ------------------------------------------------------------
# Interest Coverage Ratio
# ------------------------------------------------------------

def test_interest_coverage_normal():
    assert interest_coverage(
        500,
        100,
    ) == 5.0


def test_interest_zero_returns_none():
    assert interest_coverage(
        500,
        0,
    ) is None


# ------------------------------------------------------------
# Debt Free
# ------------------------------------------------------------

def test_debt_free_company():
    assert is_debt_free(0) is True


# ------------------------------------------------------------
# Net Debt
# ------------------------------------------------------------

def test_net_debt_normal():
    assert net_debt(
        1000,
        300,
    ) == 700


# ------------------------------------------------------------
# Asset Turnover
# ------------------------------------------------------------

def test_asset_turnover_normal():
    assert asset_turnover(
        2000,
        1000,
    ) == 2.0


def test_asset_turnover_zero_assets():
    assert asset_turnover(
        2000,
        0,
    ) is None


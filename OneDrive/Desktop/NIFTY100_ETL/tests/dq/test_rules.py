import importlib
import sys

import pandas as pd
import pytest


# ============================================================
# DAY 41 — DATA QUALITY RULE TESTS
# ============================================================


def make_tables():

    companies = pd.DataFrame({
        "id": ["TESTCO"],
        "company_name": ["Test Company"],
    })

    analysis = pd.DataFrame({
        "company_id": ["TESTCO"],
    })

    balancesheet = pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "company_id": ["TESTCO"] * 5,
        "year": [2020, 2021, 2022, 2023, 2024],
        "equity_capital": [100] * 5,
        "reserves": [100] * 5,
        "borrowings": [50] * 5,
        "other_liabilities": [50] * 5,
        "total_liabilities": [300] * 5,
        "fixed_assets": [100] * 5,
        "cwip": [20] * 5,
        "investments": [30] * 5,
        "other_asset": [150] * 5,
        "total_assets": [300] * 5,
    })

    cashflow = pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "company_id": ["TESTCO"] * 5,
        "year": [2020, 2021, 2022, 2023, 2024],
        "operating_activity": [100] * 5,
        "investing_activity": [-30] * 5,
        "financing_activity": [-20] * 5,
        "net_cash_flow": [50] * 5,
    })

    documents = pd.DataFrame({
        "id": [1],
        "company_id": ["TESTCO"],
        "Year": [2024],
        "Annual_Report": [
            "https://example.com/annual-report.pdf"
        ],
    })

    financial_ratios = pd.DataFrame({
        "id": [1],
        "company_id": ["TESTCO"],
        "year": [2024],
    })

    market_cap = pd.DataFrame({
        "id": [1],
        "company_id": ["TESTCO"],
        "year": [2024],
    })

    peer_groups = pd.DataFrame({
        "id": [1],
        "peer_group_name": ["Test Group"],
        "company_id": ["TESTCO"],
        "is_benchmark": [1],
    })

    profitandloss = pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "company_id": ["TESTCO"] * 5,
        "year": [2020, 2021, 2022, 2023, 2024],
        "sales": [1000] * 5,
        "expenses": [700] * 5,
        "operating_profit": [300] * 5,
        "opm_percentage": [30] * 5,
        "other_income": [20] * 5,
        "interest": [10] * 5,
        "depreciation": [20] * 5,
        "profit_before_tax": [290] * 5,
        "tax_percentage": [25] * 5,
        "net_profit": [217.5] * 5,
        "eps": [21.75] * 5,
        "dividend_payout": [20] * 5,
    })

    prosandcons = pd.DataFrame({
        "id": [1],
        "company_id": ["TESTCO"],
    })

    sectors = pd.DataFrame({
        "id": [1],
        "company_id": ["TESTCO"],
        "broad_sector": ["Technology"],
        "sub_sector": ["IT"],
        "index_weight_pct": [1.0],
        "market_cap_category": ["Large"],
    })

    return {
        "companies": companies,
        "analysis": analysis,
        "balancesheet": balancesheet,
        "cashflow": cashflow,
        "documents": documents,
        "financial_ratios": financial_ratios,
        "market_cap": market_cap,
        "peer_groups": peer_groups,
        "profitandloss": profitandloss,
        "prosandcons": prosandcons,
        "sectors": sectors,
    }


def run_validator(monkeypatch, tables):

    original_read_csv = pd.read_csv

    def fake_read_csv(path, *args, **kwargs):

        filename = str(path).replace("\\", "/").split("/")[-1]
        name = filename.rsplit(".", 1)[0]

        if name in tables:
            return tables[name].copy()

        return original_read_csv(path, *args, **kwargs)

    monkeypatch.setattr(pd, "read_csv", fake_read_csv)

    # Remove cached validator module so it executes again
    sys.modules.pop("src.etl.validator", None)

    validator = importlib.import_module("src.etl.validator")

    return validator.validation_failures


def has_rule(failures, rule_id, severity):

    return any(
        failure["rule"] == rule_id
        and failure["severity"] == severity
        for failure in failures
    )


# ============================================================
# DQ-01 — Company PK Uniqueness
# ============================================================

def test_dq01_duplicate_company_primary_key(monkeypatch):

    tables = make_tables()

    tables["companies"] = pd.DataFrame({
        "id": ["TESTCO", "TESTCO"],
        "company_name": ["Test Company", "Duplicate"],
    })

    failures = run_validator(monkeypatch, tables)

    assert has_rule(
        failures,
        "DQ-01",
        "CRITICAL",
    )


# ============================================================
# DQ-02 — Annual PK Uniqueness
# ============================================================

def test_dq02_duplicate_annual_record(monkeypatch):

    tables = make_tables()

    tables["profitandloss"].loc[
        4,
        "year"
    ] = 2023

    failures = run_validator(monkeypatch, tables)

    assert has_rule(
        failures,
        "DQ-02",
        "CRITICAL",
    )


# ============================================================
# DQ-03 — FK Integrity
# ============================================================

def test_dq03_invalid_company_foreign_key(monkeypatch):

    tables = make_tables()

    tables["profitandloss"].loc[
        0,
        "company_id"
    ] = "UNKNOWN"

    failures = run_validator(monkeypatch, tables)

    assert has_rule(
        failures,
        "DQ-03",
        "CRITICAL",
    )


# ============================================================
# DQ-04 — Balance Sheet Balance
# ============================================================

def test_dq04_balance_sheet_difference(monkeypatch):

    tables = make_tables()

    tables["balancesheet"].loc[
        0,
        "total_liabilities"
    ] = 250

    failures = run_validator(monkeypatch, tables)

    assert has_rule(
        failures,
        "DQ-04",
        "WARNING",
    )


# ============================================================
# DQ-05 — OPM Cross-Check
# ============================================================

def test_dq05_opm_cross_check(monkeypatch):

    tables = make_tables()

    tables["profitandloss"].loc[
        0,
        "opm_percentage"
    ] = 50

    failures = run_validator(monkeypatch, tables)

    assert has_rule(
        failures,
        "DQ-05",
        "WARNING",
    )


# ============================================================
# DQ-06 — Positive Sales
# ============================================================

def test_dq06_negative_sales(monkeypatch):

    tables = make_tables()

    tables["profitandloss"].loc[
        0,
        "sales"
    ] = -100

    failures = run_validator(monkeypatch, tables)

    assert has_rule(
        failures,
        "DQ-06",
        "WARNING",
    )


# ============================================================
# DQ-07 — Year Format Validation
# ============================================================

def test_dq07_invalid_year(monkeypatch):

    tables = make_tables()

    tables["profitandloss"].loc[
        0,
        "year"
    ] = 1800

    failures = run_validator(monkeypatch, tables)

    assert has_rule(
        failures,
        "DQ-07",
        "CRITICAL",
    )


# ============================================================
# DQ-08 — Ticker Format Validation
# ============================================================

def test_dq08_empty_ticker(monkeypatch):

    tables = make_tables()

    tables["profitandloss"].loc[
        0,
        "company_id"
    ] = " "

    failures = run_validator(monkeypatch, tables)

    assert any(
        failure.get("rule") == "DQ-08"
        and failure.get("severity") == "CRITICAL"
        for failure in failures
    )

# ============================================================
# DQ-09 — Net Cash Flow Check
# ============================================================

def test_dq09_net_cash_flow_mismatch(monkeypatch):

    tables = make_tables()

    tables["cashflow"].loc[
        0,
        "net_cash_flow"
    ] = 100

    failures = run_validator(monkeypatch, tables)

    assert has_rule(
        failures,
        "DQ-09",
        "WARNING",
    )


# ============================================================
# DQ-10 — Non-Negative Fixed Assets
# ============================================================

def test_dq10_negative_fixed_assets(monkeypatch):

    tables = make_tables()

    tables["balancesheet"].loc[
        0,
        "fixed_assets"
    ] = -100

    failures = run_validator(monkeypatch, tables)

    assert has_rule(
        failures,
        "DQ-10",
        "WARNING",
    )


# ============================================================
# DQ-11 — Tax Rate Range
# ============================================================

def test_dq11_invalid_tax_rate(monkeypatch):

    tables = make_tables()

    tables["profitandloss"].loc[
        0,
        "tax_percentage"
    ] = 75

    failures = run_validator(monkeypatch, tables)

    assert has_rule(
        failures,
        "DQ-11",
        "WARNING",
    )


# ============================================================
# DQ-12 — Dividend Payout Cap
# ============================================================

def test_dq12_dividend_payout_exceeds_cap(monkeypatch):

    tables = make_tables()

    tables["profitandloss"].loc[
        0,
        "dividend_payout"
    ] = 250

    failures = run_validator(monkeypatch, tables)

    assert has_rule(
        failures,
        "DQ-12",
        "WARNING",
    )


# ============================================================
# DQ-13 — Annual Report URL Validation
# ============================================================

def test_dq13_invalid_annual_report_url(monkeypatch):

    tables = make_tables()

    tables["documents"].loc[
        0,
        "Annual_Report"
    ] = "not-a-url"

    failures = run_validator(monkeypatch, tables)

    assert has_rule(
        failures,
        "DQ-13",
        "WARNING",
    )


# ============================================================
# DQ-14 — EPS Sign Consistency
# ============================================================

def test_dq14_positive_profit_negative_eps(monkeypatch):

    tables = make_tables()

    tables["profitandloss"].loc[
        0,
        "eps"
    ] = -10

    failures = run_validator(monkeypatch, tables)

    assert has_rule(
        failures,
        "DQ-14",
        "WARNING",
    )
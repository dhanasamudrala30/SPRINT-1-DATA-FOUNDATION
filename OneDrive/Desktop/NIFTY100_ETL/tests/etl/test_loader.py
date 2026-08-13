from pathlib import Path

import pandas as pd
import pytest

from src.etl.loader import load_excel


RAW_PATH = Path("data/raw")


# ============================================================
# DAY 41 — LOADER UNIT TESTS
# ============================================================


def test_analysis_file_loads():
    df = load_excel(RAW_PATH / "analysis.xlsx")
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_analysis_columns():
    df = load_excel(RAW_PATH / "analysis.xlsx")

    expected = {
        "company_id",
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe",
    }

    assert expected.issubset(set(df.columns))


def test_balancesheet_file_loads():
    df = load_excel(RAW_PATH / "balancesheet.xlsx")

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_balancesheet_columns():
    df = load_excel(RAW_PATH / "balancesheet.xlsx")

    expected = {
        "company_id",
        "year",
        "equity_capital",
        "reserves",
        "borrowings",
        "other_liabilities",
        "total_liabilities",
    }

    assert expected.issubset(set(df.columns))


def test_cashflow_file_loads():
    df = load_excel(RAW_PATH / "cashflow.xlsx")

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_cashflow_columns():
    df = load_excel(RAW_PATH / "cashflow.xlsx")

    expected = {
        "company_id",
        "year",
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "net_cash_flow",
    }

    assert expected.issubset(set(df.columns))


def test_companies_file_loads():
    df = load_excel(RAW_PATH / "companies.xlsx")

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_companies_columns():
    df = load_excel(RAW_PATH / "companies.xlsx")

    expected = {
        "id",
        "company_name",
        "website",
        "face_value",
        "book_value",
        "roce_percentage",
        "roe_percentage",
    }

    assert expected.issubset(set(df.columns))


def test_profitandloss_file_loads():
    df = load_excel(RAW_PATH / "profitandloss.xlsx")

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_profitandloss_columns():
    df = load_excel(RAW_PATH / "profitandloss.xlsx")

    expected = {
        "company_id",
        "year",
        "sales",
        "expenses",
        "operating_profit",
        "net_profit",
        "eps",
    }

    assert expected.issubset(set(df.columns))
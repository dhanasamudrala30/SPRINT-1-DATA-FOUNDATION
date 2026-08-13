import pandas as pd

from src.etl.normaliser import normalize_year


# ============================================================
# DAY 41 — normalize_year() UNIT TESTS
# ============================================================


def test_normalize_four_digit_year():
    assert normalize_year(2024) == 2024


def test_normalize_four_digit_year_string():
    assert normalize_year("2024") == 2024


def test_normalize_year_with_month_name():
    assert normalize_year("Mar 2015") == 2015


def test_normalize_december_year():
    assert normalize_year("Dec 2012") == 2012


def test_normalize_two_digit_year_13():
    assert normalize_year("Mar-13") == 2013


def test_normalize_two_digit_year_24():
    assert normalize_year("FY24") == 2024


def test_normalize_two_digit_year_30():
    assert normalize_year("FY30") == 2030


def test_normalize_two_digit_year_31():
    assert normalize_year("FY31") == 1931


def test_normalize_two_digit_year_99():
    assert normalize_year("FY99") == 1999


def test_normalize_two_digit_year_00():
    assert normalize_year("FY00") == 2000


def test_normalize_year_with_whitespace():
    assert normalize_year(" 2022 ") == 2022


def test_normalize_year_with_prefix():
    assert normalize_year("FY2023") == 2023


def test_normalize_year_with_suffix():
    assert normalize_year("Year 2021") == 2021


def test_normalize_year_with_month_and_year():
    assert normalize_year("April 2020") == 2020


def test_normalize_year_with_hyphen():
    assert normalize_year("2020-21") == 2020


def test_normalize_year_none():
    assert normalize_year(None) is None


def test_normalize_year_nan():
    assert normalize_year(float("nan")) is None


def test_normalize_year_pandas_nat():
    assert normalize_year(pd.NaT) is None


def test_normalize_invalid_text():
    assert normalize_year("Not a year") is None


def test_normalize_empty_string():
    assert normalize_year("") is None
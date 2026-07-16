import pytest
import sys
from pathlib import Path

# Add src/etl to Python path
sys.path.append(str(Path(__file__).resolve().parents[2] / "src" / "etl"))

from normaliser import normalize_year, normalize_ticker


# -----------------------------
# normalize_year() Tests
# -----------------------------

def test_year_1():
    assert normalize_year("Mar 2015") == 2015

def test_year_2():
    assert normalize_year("Dec 2012") == 2012

def test_year_3():
    assert normalize_year("2020") == 2020

def test_year_4():
    assert normalize_year("Mar-13") == 2013

def test_year_5():
    assert normalize_year("Mar-99") == 1999

def test_year_6():
    assert normalize_year(None) is None

def test_year_7():
    assert normalize_year("") is None

def test_year_8():
    assert normalize_year("Invalid") is None

def test_year_9():
    assert normalize_year("FY2024") == 2024

def test_year_10():
    assert normalize_year("2018") == 2018


# -----------------------------
# normalize_ticker() Tests
# -----------------------------

def test_ticker_1():
    assert normalize_ticker("tcs") == "TCS"

def test_ticker_2():
    assert normalize_ticker(" TCS ") == "TCS"

def test_ticker_3():
    assert normalize_ticker("HdfcBank") == "HDFCBANK"

def test_ticker_4():
    assert normalize_ticker("abb") == "ABB"

def test_ticker_5():
    assert normalize_ticker(" Reliance ") == "RELIANCE"

def test_ticker_6():
    assert normalize_ticker("") == ""

def test_ticker_7():
    assert normalize_ticker(None) is None

def test_ticker_8():
    assert normalize_ticker("icicibank") == "ICICIBANK"

def test_ticker_9():
    assert normalize_ticker("axisbank") == "AXISBANK"

def test_ticker_10():
    assert normalize_ticker("sbilife") == "SBILIFE"
import pandas as pd
import re


def normalize_year(year):
    """
    Normalize different year formats into YYYY.
    Examples:
    Mar 2015 -> 2015
    Dec 2012 -> 2012
    Mar-13   -> 2013
    2020     -> 2020
    """

    if pd.isna(year):
        return None

    year = str(year).strip()

    # Match four-digit year
    match = re.search(r"(20\d{2}|19\d{2})", year)

    if match:
        return int(match.group())

    # Match two-digit year
    match = re.search(r"(\d{2})$", year)

    if match:
        yy = int(match.group())

        if yy <= 30:
            return 2000 + yy
        else:
            return 1900 + yy

    return None


def normalize_ticker(ticker):
    """
    Standardize company ticker names.
    """

    if pd.isna(ticker):
        return None

    return str(ticker).strip().upper()
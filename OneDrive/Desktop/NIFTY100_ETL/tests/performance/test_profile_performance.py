import time

from src.dashboard.utils.db import get_companies, get_ratios


TICKERS = [
    "TCS",
    "INFY",
    "RELIANCE",
    "HDFCBANK",
    "ITC",
]


def test_company_profile_performance():

    companies = get_companies()
    ratios = get_ratios()

    print("\n" + "=" * 60)
    print("DAY 43 — COMPANY PROFILE PERFORMANCE")
    print("=" * 60)

    for ticker in TICKERS:

        start = time.perf_counter()

        company_df = ratios[
            ratios["company_id"] == ticker
        ].sort_values("year")

        elapsed = time.perf_counter() - start

        print(
            f"{ticker:12} | "
            f"Rows: {len(company_df):2d} | "
            f"Load time: {elapsed:.4f}s"
        )

        assert ticker in companies
        assert not company_df.empty
        assert elapsed < 3.0

    print("=" * 60)
    print("All 5 company profiles completed under 3 seconds")
    print("=" * 60)
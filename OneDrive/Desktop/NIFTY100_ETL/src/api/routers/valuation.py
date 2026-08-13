# from fastapi import APIRouter

# router = APIRouter()


# @router.get("/")
# def valuation():

#     return {
#         "message": "Valuation API"
#     }

import sqlite3
from pathlib import Path

from fastapi import APIRouter, HTTPException


router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / "nifty100.db"


def get_connection():
    """Create and return a database connection."""

    connection = sqlite3.connect(str(DB_PATH))
    connection.row_factory = sqlite3.Row

    return connection


@router.get("/{ticker}")
def get_market_cap_history(
    ticker: str,
):

    """Return historical valuation and market-cap data."""
    ticker = ticker.strip().upper()

    connection = get_connection()

    company = connection.execute(
        """
        SELECT id, company_name
        FROM companies
        WHERE UPPER(TRIM(id)) = ?
        LIMIT 1
        """,
        (ticker,),
    ).fetchone()

    if company is None:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found",
        )

    rows = connection.execute(
        """
        SELECT
            year,
            market_cap_crore,
            enterprise_value_crore,
            pe_ratio,
            pb_ratio,
            ev_ebitda,
            dividend_yield_pct

        FROM market_cap

        WHERE UPPER(TRIM(company_id)) = ?

        AND year BETWEEN 2019 AND 2024

        ORDER BY year
        """,
        (ticker,),
    ).fetchall()

    connection.close()

    return {
        "company_id": ticker,
        "company_name": company["company_name"],
        "count": len(rows),
        "history": [
            dict(row)
            for row in rows
        ],
    }
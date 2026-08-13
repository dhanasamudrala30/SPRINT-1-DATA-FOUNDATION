# from fastapi import APIRouter

# router = APIRouter()


# @router.get("/")
# def get_sectors():

#     return {
#         "message": "Sectors API"
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


# ============================================================
# GET ALL SECTORS
# ============================================================

@router.get("/")
def get_sectors():

    """Return sector-level financial statistics."""
    connection = get_connection()

    query = """
        WITH latest_ratios AS (
            SELECT *
            FROM financial_ratios r
            WHERE year = (
                SELECT MAX(r2.year)
                FROM financial_ratios r2
                WHERE r2.company_id = r.company_id
            )
        ),

        latest_market AS (
            SELECT *
            FROM market_cap mc
            WHERE year = (
                SELECT MAX(mc2.year)
                FROM market_cap mc2
                WHERE mc2.company_id = mc.company_id
            )
        )

        SELECT
            s.broad_sector,

            COUNT(DISTINCT s.company_id)
                AS company_count,

            ROUND(
                AVG(r.return_on_equity_pct),
                2
            ) AS median_roe,

            ROUND(
                AVG(mc.pe_ratio),
                2
            ) AS median_pe,

            ROUND(
                AVG(r.debt_to_equity),
                2
            ) AS median_de

        FROM sectors s

        LEFT JOIN latest_ratios r
            ON UPPER(TRIM(s.company_id))
            =
            UPPER(TRIM(r.company_id))

        LEFT JOIN latest_market mc
            ON UPPER(TRIM(s.company_id))
            =
            UPPER(TRIM(mc.company_id))

        GROUP BY s.broad_sector

        ORDER BY s.broad_sector
    """

    rows = connection.execute(query).fetchall()

    connection.close()

    return {
        "count": len(rows),
        "data": [dict(row) for row in rows],
    }


# ============================================================
# GET COMPANIES IN SECTOR
# ============================================================

@router.get("/{sector}/companies")
def get_sector_companies(
    sector: str,
):

    """Return companies belonging to a sector."""
    connection = get_connection()

    # First verify sector exists

    sector_exists = connection.execute(
        """
        SELECT 1
        FROM sectors
        WHERE LOWER(TRIM(broad_sector))
              =
              LOWER(TRIM(?))
        LIMIT 1
        """,
        (sector,),
    ).fetchone()

    if sector_exists is None:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Sector '{sector}' not found",
        )

    query = """
        WITH latest_ratios AS (
            SELECT *
            FROM financial_ratios r
            WHERE year = (
                SELECT MAX(r2.year)
                FROM financial_ratios r2
                WHERE r2.company_id = r.company_id
            )
        )

        SELECT
            c.id AS company_id,
            c.company_name,

            s.broad_sector,
            s.sub_sector,
            s.market_cap_category,

            r.year,

            r.return_on_equity_pct AS roe_pct,
            r.debt_to_equity,
            r.free_cash_flow_cr,
            r.operating_profit_margin_pct,
            r.interest_coverage,
            r.asset_turnover

        FROM sectors s

        JOIN companies c
            ON UPPER(TRIM(c.id))
            =
            UPPER(TRIM(s.company_id))

        LEFT JOIN latest_ratios r
            ON UPPER(TRIM(c.id))
            =
            UPPER(TRIM(r.company_id))

        WHERE LOWER(TRIM(s.broad_sector))
              =
              LOWER(TRIM(?))

        ORDER BY c.id
    """

    rows = connection.execute(
        query,
        (sector,),
    ).fetchall()

    connection.close()

    return {
        "sector": sector,
        "count": len(rows),
        "data": [dict(row) for row in rows],
    }
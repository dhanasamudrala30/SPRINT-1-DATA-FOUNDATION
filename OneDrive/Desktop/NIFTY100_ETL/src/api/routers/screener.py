# from fastapi import APIRouter

# router = APIRouter()


# @router.get("/")
# def screener():

#     return {
#         "message": "Screener API"
#     }



import sqlite3
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query


router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / "nifty100.db"


def get_connection():
    """Create and return a database connection."""
    connection = sqlite3.connect(str(DB_PATH))
    connection.row_factory = sqlite3.Row
    return connection


@router.get("/")
def screen_companies(
    min_roe: Optional[str] = Query(None),
max_de: Optional[str] = Query(None),
min_fcf: Optional[str] = Query(None),
sector: Optional[str] = Query(None),
min_rev_cagr_5yr: Optional[str] = Query(None),
min_pat_cagr_5yr: Optional[str] = Query(None),
max_pe: Optional[str] = Query(None),
):

    # --------------------------------------------------------
    # Convert and validate numeric parameters
    # --------------------------------------------------------

    """Screen and rank companies using financial filters."""
    def parse_float(value, parameter_name):
        """Parse and validate a numeric API parameter."""
        if value is None:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=400,
                detail=f"{parameter_name} must be a valid number",
            )

    min_roe = parse_float(min_roe, "min_roe")
    max_de = parse_float(max_de, "max_de")
    min_fcf = parse_float(min_fcf, "min_fcf")
    min_rev_cagr_5yr = parse_float(
        min_rev_cagr_5yr,
        "min_rev_cagr_5yr",
    )
    min_pat_cagr_5yr = parse_float(
        min_pat_cagr_5yr,
        "min_pat_cagr_5yr",
    )
    max_pe = parse_float(max_pe, "max_pe")

    """
    Screen companies using latest available financial metrics.
    """

    # --------------------------------------------------------
    # Validate parameters
    # --------------------------------------------------------

    if min_roe is not None and min_roe < -100:
        raise HTTPException(
            status_code=400,
            detail="min_roe cannot be less than -100",
        )

    if max_de is not None and max_de < 0:
        raise HTTPException(
            status_code=400,
            detail="max_de cannot be negative",
        )

    if max_pe is not None and max_pe <= 0:
        raise HTTPException(
            status_code=400,
            detail="max_pe must be greater than 0",
        )

    connection = get_connection()

    # --------------------------------------------------------
    # Latest financial ratios
    # --------------------------------------------------------

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

        latest_metrics AS (
            SELECT *
            FROM financial_metrics m
            WHERE end_year = (
                SELECT MAX(m2.end_year)
                FROM financial_metrics m2
                WHERE m2.company_id = m.company_id
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
            c.id AS company_id,
            c.company_name,

            s.broad_sector,
            s.sub_sector,
            s.market_cap_category,

            r.year AS ratio_year,

            r.return_on_equity_pct AS roe_pct,
            r.debt_to_equity AS debt_to_equity,
            r.free_cash_flow_cr AS fcf_cr,
            r.operating_profit_margin_pct AS operating_profit_margin_pct,

            m.end_year AS metric_year,
            m.revenue_cagr_5yr,
            m.pat_cagr_5yr,

            mc.year AS valuation_year,
            mc.pe_ratio,
            mc.pb_ratio,
            mc.ev_ebitda,
            mc.dividend_yield_pct

        FROM companies c

        LEFT JOIN latest_ratios r
            ON UPPER(TRIM(c.id))
            =
            UPPER(TRIM(r.company_id))

        LEFT JOIN latest_metrics m
            ON UPPER(TRIM(c.id))
            =
            UPPER(TRIM(m.company_id))

        LEFT JOIN latest_market mc
            ON UPPER(TRIM(c.id))
            =
            UPPER(TRIM(mc.company_id))

        LEFT JOIN sectors s
            ON UPPER(TRIM(c.id))
            =
            UPPER(TRIM(s.company_id))

        WHERE 1 = 1
    """

    params = []

    # --------------------------------------------------------
    # Filters
    # --------------------------------------------------------

    if min_roe is not None:
        query += """
            AND r.return_on_equity_pct >= ?
        """
        params.append(min_roe)

    if max_de is not None:
        query += """
            AND r.debt_to_equity <= ?
        """
        params.append(max_de)

    if min_fcf is not None:
        query += """
            AND r.free_cash_flow_cr >= ?
        """
        params.append(min_fcf)

    if sector:
        query += """
            AND LOWER(TRIM(s.broad_sector))
                = LOWER(TRIM(?))
        """
        params.append(sector)

    if min_rev_cagr_5yr is not None:
        query += """
            AND m.revenue_cagr_5yr >= ?
        """
        params.append(min_rev_cagr_5yr)

    if min_pat_cagr_5yr is not None:
        query += """
            AND m.pat_cagr_5yr >= ?
        """
        params.append(min_pat_cagr_5yr)

    if max_pe is not None:
        query += """
            AND mc.pe_ratio <= ?
        """
        params.append(max_pe)

    query += """
        ORDER BY
            COALESCE(r.return_on_equity_pct, -999)
            DESC
    """

    rows = connection.execute(
        query,
        params,
    ).fetchall()

    connection.close()

    return {
        "count": len(rows),
        "data": [dict(row) for row in rows],
    }
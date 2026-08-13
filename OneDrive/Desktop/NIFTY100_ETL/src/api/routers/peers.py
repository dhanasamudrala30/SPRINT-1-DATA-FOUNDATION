# from fastapi import APIRouter

# router = APIRouter()


# @router.get("/")
# def get_peers():

#     return {
#         "message": "Peers API"
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


@router.get("/{group_name}")
def get_peer_group(group_name: str):

    """Return companies belonging to a peer group."""
    connection = get_connection()

    # Check whether peer group exists
    group = connection.execute(
        """
        SELECT DISTINCT peer_group_name
        FROM peer_groups
        WHERE LOWER(TRIM(peer_group_name))
              =
              LOWER(TRIM(?))
        LIMIT 1
        """,
        (group_name,),
    ).fetchone()

    if group is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Peer group '{group_name}' not found",
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
            pg.peer_group_name,
            pg.company_id,
            pg.is_benchmark,

            c.company_name,

            r.return_on_equity_pct,
            r.debt_to_equity,
            r.operating_profit_margin_pct,
            r.net_profit_margin_pct,
            r.interest_coverage,
            r.asset_turnover,
            r.free_cash_flow_cr,
            r.earnings_per_share,
            r.dividend_payout_ratio_pct,
            r.free_cash_flow_cr AS fcf_cr

        FROM peer_groups pg

        LEFT JOIN companies c
            ON UPPER(TRIM(pg.company_id))
            =
            UPPER(TRIM(c.id))

        LEFT JOIN latest_ratios r
            ON UPPER(TRIM(pg.company_id))
            =
            UPPER(TRIM(r.company_id))

        WHERE LOWER(TRIM(pg.peer_group_name))
              =
              LOWER(TRIM(?))

        ORDER BY pg.is_benchmark DESC, pg.company_id
    """

    rows = connection.execute(
        query,
        (group_name,),
    ).fetchall()

    connection.close()

    data = [dict(row) for row in rows]

    # --------------------------------------------------------
    # Calculate percentile ranks
    # --------------------------------------------------------

    metrics = [
        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "net_profit_margin_pct",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "earnings_per_share",
        "dividend_payout_ratio_pct",
        "fcf_cr",
    ]

    for metric in metrics:

        values = [
            row[metric]
            for row in data
            if row[metric] is not None
        ]

        if not values:
            continue

        sorted_values = sorted(values)
        n = len(sorted_values)
        for row in data:

            value = row[metric]

            if value is None:
                row[f"{metric}_percentile"] = None
                continue

            less_equal = sum(
                x <= value
                for x in sorted_values
            )

            percentile = (
                less_equal / n
            ) * 100

            row[
                f"{metric}_percentile"
            ] = round(percentile, 2)

    return {
        "peer_group": group_name,
        "count": len(data),
        "data": data,
    }
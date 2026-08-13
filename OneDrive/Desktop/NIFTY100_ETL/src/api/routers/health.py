import sqlite3
import time

from fastapi import APIRouter

router = APIRouter()

START_TIME = time.time()

DB_PATH = "nifty100.db"


TABLES = [
    "analysis",
    "balancesheet",
    "cashflow",
    "companies",
    "documents",
    "financial_ratios",
    "market_cap",
    "peer_groups",
    "profitandloss",
    "sectors",
]


@router.get("/health")
def health_check():

    """Return API health status and database statistics."""
    db_row_counts = {}

    try:
        connection = sqlite3.connect(DB_PATH)

        for table in TABLES:

            result = connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()

            db_row_counts[table] = result[0]

        connection.close()

        db_status = "ok"

    except Exception as e:

        db_status = f"error: {str(e)}"

    uptime = round(
        time.time() - START_TIME,
        2
    )

    return {
        "status": "ok",
        "database": db_status,
        "db_row_counts": db_row_counts,
        "uptime_seconds": uptime,
        "version": "1.0.0",
    }
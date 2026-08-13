# from fastapi import APIRouter

# router = APIRouter()


# @router.get("/")
# def portfolio():

#     return {
#         "message": "Portfolio API"
#     }

import pandas as pd
from pathlib import Path

from fastapi import APIRouter, HTTPException


router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]

STATS_FILE = (
    PROJECT_ROOT
    / "output"
    / "portfolio_stats.csv"
)


@router.get("/stats")
def get_portfolio_stats():

    """Return portfolio KPI percentile statistics."""
    if not STATS_FILE.exists():

        raise HTTPException(
            status_code=404,
            detail="Portfolio statistics file not found",
        )

    df = pd.read_csv(STATS_FILE)

    return {
        "count": len(df),
        "data": df.to_dict(
            orient="records"
        ),
    }
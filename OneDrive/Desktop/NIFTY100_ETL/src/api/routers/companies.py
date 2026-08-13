# from fastapi import APIRouter

# router = APIRouter()


# @router.get("/")
# def get_companies():

#     return {
#         "message": "Companies API"
#     }


import sqlite3
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse


router = APIRouter()


# ============================================================
# DATABASE
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "nifty100.db"


def get_connection():
    """Create and return a database connection."""

    connection = sqlite3.connect(
        str(DB_PATH)
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# HELPERS
# ============================================================

def row_to_dict(row):

    """Convert a database row into a dictionary."""
    if row is None:
        return None

    return dict(row)


def clean_ticker(ticker: str):

    """Normalize a ticker value for API processing."""
    return ticker.strip().upper()


def company_exists(connection, ticker):

    """Check whether a company exists in the database."""
    row = connection.execute(
        """
        SELECT id
        FROM companies
        WHERE UPPER(TRIM(id)) = ?
        """,
        (ticker,),
    ).fetchone()

    return row is not None


def apply_year_filter(
    query,
    params,
    date_column,
    from_year,
    to_year,
):

    """Apply optional year-range filtering to a database query."""
    if from_year:

        query += f"""
        AND {date_column} >= ?
        """

        params.append(
            from_year
        )

    if to_year:

        query += f"""
        AND {date_column} <= ?
        """

        params.append(
            to_year
        )

    return query, params


# ============================================================
# 1. GET ALL COMPANIES
# ============================================================

@router.get("/")
def get_companies(
    sector: Optional[str] = Query(
        None,
        description="Filter by broad sector",
    ),

    market_cap_category: Optional[str] = Query(
        None,
        description="Filter by market cap category",
    ),

    search: Optional[str] = Query(
        None,
        description="Partial company name or ticker search",
    ),
):

    """Return the company list with available financial information."""
    connection = get_connection()

    query = """
        SELECT
            c.id,
            c.company_name,
            s.broad_sector,
            s.sub_sector,
            c.roe_percentage AS roe_pct,
            c.roce_percentage AS roce_pct
        FROM companies c
        LEFT JOIN sectors s
            ON UPPER(TRIM(c.id))
            =
            UPPER(TRIM(s.company_id))
        WHERE 1 = 1
    """

    params = []

    # --------------------------------------------------------
    # Sector filter
    # --------------------------------------------------------

    if sector:

        query += """
            AND LOWER(s.broad_sector)
            =
            LOWER(?)
        """

        params.append(
            sector.strip()
        )

    # --------------------------------------------------------
    # Market cap filter
    # --------------------------------------------------------

    if market_cap_category:

        query += """
            AND LOWER(s.market_cap_category)
            =
            LOWER(?)
        """

        params.append(
            market_cap_category.strip()
        )

    # --------------------------------------------------------
    # Search filter
    # --------------------------------------------------------

    if search:

        query += """
            AND (
                LOWER(c.id) LIKE LOWER(?)
                OR
                LOWER(c.company_name) LIKE LOWER(?)
            )
        """

        search_pattern = (
            f"%{search.strip()}%"
        )

        params.extend(
            [
                search_pattern,
                search_pattern,
            ]
        )

    query += """
        ORDER BY c.id
    """

    rows = connection.execute(
        query,
        params,
    ).fetchall()

    connection.close()

    return {
        "count": len(rows),
        "data": [
            row_to_dict(row)
            for row in rows
        ],
    }


# ============================================================
# 2. GET FULL COMPANY PROFILE
# ============================================================

@router.get("/{ticker}")
def get_company(
    ticker: str,
):

    """Return the complete profile for a company."""
    ticker = clean_ticker(ticker)

    connection = get_connection()

    # --------------------------------------------------------
    # Company profile + sector
    # --------------------------------------------------------

    row = connection.execute(
        """
        SELECT
            c.*,

            s.broad_sector,
            s.sub_sector,
            s.index_weight_pct,
            s.market_cap_category

        FROM companies c

        LEFT JOIN sectors s
            ON UPPER(TRIM(c.id))
            =
            UPPER(TRIM(s.company_id))

        WHERE UPPER(TRIM(c.id)) = ?

        LIMIT 1
        """,
        (ticker,),
    ).fetchone()

    if row is None:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found",
        )

    company = row_to_dict(row)

    # --------------------------------------------------------
    # Latest financial ratios
    # --------------------------------------------------------

    latest_ratios = connection.execute(
        """
        SELECT *
        FROM financial_ratios
        WHERE UPPER(TRIM(company_id)) = ?
        ORDER BY year DESC
        LIMIT 1
        """,
        (ticker,),
    ).fetchone()

    company["latest_kpis"] = (
        row_to_dict(latest_ratios)
        if latest_ratios
        else {}
    )

    connection.close()

    return company


# ============================================================
# 3. P&L HISTORY
# ============================================================

@router.get("/{ticker}/pl")
def get_profit_loss(
    ticker: str,

    from_year: Optional[str] = Query(
        None,
        description="Start year in YYYY-MM format",
    ),

    to_year: Optional[str] = Query(
        None,
        description="End year in YYYY-MM format",
    ),
):

    """Return profit-and-loss history for a company."""
    ticker = clean_ticker(ticker)

    connection = get_connection()

    if not company_exists(
        connection,
        ticker,
    ):

        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found",
        )

    query = """
        SELECT *
        FROM profitandloss
        WHERE UPPER(TRIM(company_id)) = ?
    """

    params = [
        ticker
    ]

    query, params = apply_year_filter(
        query,
        params,
        "year",
        from_year,
        to_year,
    )

    query += """
        ORDER BY year
    """

    rows = connection.execute(
        query,
        params,
    ).fetchall()

    connection.close()

    return {
        "company_id": ticker,
        "count": len(rows),
        "history": [
            row_to_dict(row)
            for row in rows
        ],
    }


# ============================================================
# 4. BALANCE SHEET HISTORY
# ============================================================

@router.get("/{ticker}/bs")
def get_balance_sheet(
    ticker: str,

    from_year: Optional[str] = Query(
        None,
        description="Start year in YYYY-MM format",
    ),

    to_year: Optional[str] = Query(
        None,
        description="End year in YYYY-MM format",
    ),
):

    """Return balance-sheet history for a company."""
    ticker = clean_ticker(ticker)

    connection = get_connection()

    if not company_exists(
        connection,
        ticker,
    ):

        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found",
        )

    query = """
        SELECT *
        FROM balancesheet
        WHERE UPPER(TRIM(company_id)) = ?
    """

    params = [
        ticker
    ]

    query, params = apply_year_filter(
        query,
        params,
        "year",
        from_year,
        to_year,
    )

    query += """
        ORDER BY year
    """

    rows = connection.execute(
        query,
        params,
    ).fetchall()

    connection.close()

    return {
        "company_id": ticker,
        "count": len(rows),
        "history": [
            row_to_dict(row)
            for row in rows
        ],
    }


# ============================================================
# 5. CASH FLOW HISTORY
# ============================================================

@router.get("/{ticker}/cashflow")
def get_cashflow(
    ticker: str,

    from_year: Optional[str] = Query(
        None,
        description="Start year in YYYY-MM format",
    ),

    to_year: Optional[str] = Query(
        None,
        description="End year in YYYY-MM format",
    ),
):

    """Return cash-flow history for a company."""
    ticker = clean_ticker(ticker)

    connection = get_connection()

    if not company_exists(
        connection,
        ticker,
    ):

        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found",
        )

    query = """
        SELECT *
        FROM cashflow
        WHERE UPPER(TRIM(company_id)) = ?
    """

    params = [
        ticker
    ]

    query, params = apply_year_filter(
        query,
        params,
        "year",
        from_year,
        to_year,
    )

    query += """
        ORDER BY year
    """

    rows = connection.execute(
        query,
        params,
    ).fetchall()

    connection.close()

    return {
        "company_id": ticker,
        "count": len(rows),
        "history": [
            row_to_dict(row)
            for row in rows
        ],
    }


# ============================================================
# 6. FINANCIAL RATIOS
# ============================================================

@router.get("/{ticker}/ratios")
def get_ratios(
    ticker: str,

    year: Optional[int] = Query(
        None,
        description="Return ratios for a specific year",
    ),
):

    """Return calculated financial ratios for a company."""
    ticker = clean_ticker(ticker)

    connection = get_connection()

    if not company_exists(
        connection,
        ticker,
    ):

        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found",
        )

    query = """
        SELECT *
        FROM financial_ratios
        WHERE UPPER(TRIM(company_id)) = ?
    """

    params = [
        ticker
    ]

    if year is not None:

        query += """
            AND year = ?
        """

        params.append(
            year
        )

    query += """
        ORDER BY year
    """

    rows = connection.execute(
        query,
        params,
    ).fetchall()

    connection.close()

    return {
        "company_id": ticker,
        "count": len(rows),
        "data": [
            row_to_dict(row)
            for row in rows
        ],
    }


# ============================================================
# 7. COMPANY TEARSHEET PDF
# ============================================================

@router.get("/{ticker}/tearsheet")
def get_tearsheet(
    ticker: str,
):

    """Return the company's PDF tearsheet."""
    ticker = clean_ticker(ticker)

    connection = get_connection()

    if not company_exists(
        connection,
        ticker,
    ):

        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found",
        )

    connection.close()

    tearsheet_path = (
        PROJECT_ROOT
        / "reports"
        / "tearsheets"
        / f"{ticker}_tearsheet.pdf"
    )

    if not tearsheet_path.exists():

        raise HTTPException(
            status_code=404,
            detail=(
                f"Tearsheet for '{ticker}' "
                "is not available"
            ),
        )

    return FileResponse(
        path=str(tearsheet_path),
        media_type="application/pdf",
        filename=(
            f"{ticker}_tearsheet.pdf"
        ),
    )

# ============================================================
# PEER RADAR COMPARISON
# ============================================================

@router.get("/{ticker}/peers/compare")
def compare_with_peers(
    ticker: str,
):

    """Return company and peer comparison data."""
    ticker = clean_ticker(ticker)

    connection = get_connection()

    # --------------------------------------------------------
    # Check company
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Find peer group
    # --------------------------------------------------------

    peer_group = connection.execute(
        """
        SELECT peer_group_name
        FROM peer_groups
        WHERE UPPER(TRIM(company_id)) = ?
        LIMIT 1
        """,
        (ticker,),
    ).fetchone()

    if peer_group is None:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"No peer group found for '{ticker}'",
        )

    group_name = peer_group["peer_group_name"]

    # --------------------------------------------------------
    # Latest ratios for peer group
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
        )

        SELECT
            pg.company_id,
            pg.is_benchmark,

            r.return_on_equity_pct,
            r.debt_to_equity,
            r.operating_profit_margin_pct,
            r.net_profit_margin_pct,
            r.interest_coverage,
            r.asset_turnover,
            r.free_cash_flow_cr,
            r.earnings_per_share

        FROM peer_groups pg

        LEFT JOIN latest_ratios r
            ON UPPER(TRIM(pg.company_id))
            =
            UPPER(TRIM(r.company_id))

        WHERE LOWER(TRIM(pg.peer_group_name))
              =
              LOWER(TRIM(?))
    """

    rows = connection.execute(
        query,
        (group_name,),
    ).fetchall()

    connection.close()

    data = [dict(row) for row in rows]

    axes = [
        (
            "ROE",
            "return_on_equity_pct",
        ),
        (
            "Debt to Equity",
            "debt_to_equity",
        ),
        (
            "Operating Margin",
            "operating_profit_margin_pct",
        ),
        (
            "Net Margin",
            "net_profit_margin_pct",
        ),
        (
            "Interest Coverage",
            "interest_coverage",
        ),
        (
            "Asset Turnover",
            "asset_turnover",
        ),
        (
            "Free Cash Flow",
            "free_cash_flow_cr",
        ),
        (
            "EPS",
            "earnings_per_share",
        ),
    ]

    company_row = None
    benchmark_row = None

    for row in data:

        if row["company_id"] == ticker:
            company_row = row

        if row["is_benchmark"]:
            benchmark_row = row

    if company_row is None:

        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found in peer group",
        )

    radar = []

    for label, field in axes:

        values = [
            row[field]
            for row in data
            if row[field] is not None
        ]

        average = (
            sum(values) / len(values)
            if values
            else None
        )

        radar.append(
            {
                "metric": label,
                "company": company_row[field],
                "peer_group_average": (
                    round(average, 2)
                    if average is not None
                    else None
                ),
                "benchmark": (
                    benchmark_row[field]
                    if benchmark_row
                    else None
                ),
            }
        )

    return {
        "company_id": ticker,
        "company_name": company["company_name"],
        "peer_group": group_name,
        "radar": radar,
    }
# ============================================================
# COMPANY DOCUMENTS
# ============================================================

@router.get("/{ticker}/documents")
def get_company_documents(
    ticker: str,
):

    """Return annual-report documents for a company."""
    ticker = clean_ticker(ticker)

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
            Year AS year,
            Annual_Report AS annual_report
        FROM documents
        WHERE UPPER(TRIM(company_id)) = ?
        ORDER BY Year DESC
        """,
        (ticker,),
    ).fetchall()

    connection.close()

    documents = []

    for row in rows:

        url = row["annual_report"]

        # Basic URL validation without making
        # external network requests.
        is_valid = (
            isinstance(url, str)
            and url.startswith(
                (
                    "http://",
                    "https://",
                )
            )
        )

        documents.append(
            {
                "year": row["year"],
                "annual_report": url,
                "is_url_valid": is_valid,
            }
        )

    return {
        "company_id": ticker,
        "company_name": company["company_name"],
        "count": len(documents),
        "documents": documents,
    }
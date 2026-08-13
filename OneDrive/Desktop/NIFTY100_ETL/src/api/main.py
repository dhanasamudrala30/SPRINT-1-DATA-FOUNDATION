import logging
import sqlite3
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


from src.api.routers import (
    companies,
    screener,
    sectors,
    peers,
    valuation,
    portfolio,
    documents,
    health,
)


# ============================================================
# CONFIGURATION
# ============================================================

DB_PATH = "nifty100.db"

VERSION = "1.0.0"


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection():

    """Create and return a database connection."""
    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="NIFTY 100 Analytics API",
    description="FastAPI REST API for NIFTY 100 financial analytics",
    version=VERSION,
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST LOGGING MIDDLEWARE
# ============================================================

@app.middleware("http")
async def request_logging_middleware(
    request: Request,
    call_next,
):

    """Log HTTP request method, path, status, and response time."""
    start_time = time.perf_counter()

    response = await call_next(
        request
    )

    elapsed = (
        time.perf_counter() - start_time
    )

    logger.info(
        "%s %s - %s - %.4f sec",
        request.method,
        request.url.path,
        response.status_code,
        elapsed,
    )

    return response


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    """Return basic API information."""
    return {
        "message": "NIFTY 100 Analytics API",
        "version": VERSION,
        "docs": "/docs",
    }


# ============================================================
# ROUTERS
# ============================================================

API_PREFIX = "/api/v1"


app.include_router(
    companies.router,
    prefix=f"{API_PREFIX}/companies",
    tags=["Companies"],
)

app.include_router(
    screener.router,
    prefix=f"{API_PREFIX}/screener",
    tags=["Screener"],
)

app.include_router(
    sectors.router,
    prefix=f"{API_PREFIX}/sectors",
    tags=["Sectors"],
)

app.include_router(
    peers.router,
    prefix=f"{API_PREFIX}/peers",
    tags=["Peers"],
)

app.include_router(
    valuation.router,
    prefix=f"{API_PREFIX}/valuation",
    tags=["Valuation"],
)

app.include_router(
    portfolio.router,
    prefix=f"{API_PREFIX}/portfolio",
    tags=["Portfolio"],
)

app.include_router(
    documents.router,
    prefix=f"{API_PREFIX}/documents",
    tags=["Documents"],
)

app.include_router(
    health.router,
    prefix=API_PREFIX,
    tags=["Health"],
)
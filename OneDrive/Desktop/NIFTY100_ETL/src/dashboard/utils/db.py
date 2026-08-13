import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

# CSV Files
RATIOS = PROJECT_ROOT / "data" / "processed" / "financial_ratios.csv"
METRICS = PROJECT_ROOT / "data" / "processed" / "financial_metrics.csv"
PEERS = PROJECT_ROOT / "data" / "processed" / "peer_groups.csv"


@st.cache_data(ttl=600)
def get_companies():
    """Return the company list with available financial information."""
    companies = (
        pd.read_csv(RATIOS)["company_id"]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )
    return companies


@st.cache_data(ttl=600)
def get_ratios():
    """Return calculated financial ratios for a company."""
    return pd.read_csv(RATIOS)


@st.cache_data(ttl=600)
def get_metrics():
    """Load financial metrics for the dashboard."""
    return pd.read_csv(METRICS)


@st.cache_data(ttl=600)
def get_peers():
    """Load peer-group data for the dashboard."""
    return pd.read_csv(PEERS)


@st.cache_data(ttl=600)
def get_peer_percentiles():
    """Load peer percentile data for the dashboard."""
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM peer_percentiles",
        conn
    )

    conn.close()

    return df
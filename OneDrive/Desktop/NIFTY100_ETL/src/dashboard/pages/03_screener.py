import streamlit as st
import pandas as pd

from utils.db import get_metrics

st.title(" Financial Screener")

st.write("Filter companies based on financial performance.")

# -----------------------
# Load Data
# -----------------------
metrics = get_metrics()

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Filters")

min_roce = st.sidebar.slider(
    "Minimum ROCE (%)",
    0.0,
    100.0,
    10.0
)

min_revenue = st.sidebar.slider(
    "Minimum Revenue CAGR (%)",
    0.0,
    100.0,
    10.0
)

min_pat = st.sidebar.slider(
    "Minimum PAT CAGR (%)",
    0.0,
    100.0,
    10.0
)

# -----------------------
# Apply Filters
# -----------------------
filtered = metrics[
    (metrics["roce_pct"].fillna(0) >= min_roce) &
    (metrics["revenue_cagr_5yr"].fillna(0) >= min_revenue) &
    (metrics["pat_cagr_5yr"].fillna(0) >= min_pat)
]

# -----------------------
# Results
# -----------------------
st.subheader("Matching Companies")

st.metric("Companies Found", len(filtered))

st.dataframe(filtered, use_container_width=True)

# -----------------------
# Download
# -----------------------
csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label=" Download Results",
    data=csv,
    file_name="financial_screener.csv",
    mime="text/csv",
)
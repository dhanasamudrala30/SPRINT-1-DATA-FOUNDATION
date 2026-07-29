import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_companies,
    get_metrics,
    get_peers,
)

st.title(" Home Dashboard")

# -----------------------------
# Load Data
# -----------------------------
companies = get_companies()
metrics = get_metrics()
peers = get_peers()

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Companies", len(companies))
col2.metric("Peer Groups", peers["peer_group_name"].nunique())
col3.metric("Average ROCE", f"{metrics['roce_pct'].mean():.2f}%")
col4.metric(
    "Average Revenue CAGR",
    f"{metrics['revenue_cagr_5yr'].mean():.2f}%"
)

st.divider()

# -----------------------------
# Company Selector
# -----------------------------
selected_company = st.selectbox(
    "Select a Company",
    companies
)

company = metrics[metrics["company_id"] == selected_company]

if not company.empty:

    st.subheader(f"{selected_company} Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Revenue CAGR",
        f"{company.iloc[0]['revenue_cagr_5yr']:.2f}%"
        if pd.notna(company.iloc[0]["revenue_cagr_5yr"])
        else "N/A"
    )

    c2.metric(
        "PAT CAGR",
        f"{company.iloc[0]['pat_cagr_5yr']:.2f}%"
        if pd.notna(company.iloc[0]["pat_cagr_5yr"])
        else "N/A"
    )

    c3.metric(
        "EPS CAGR",
        f"{company.iloc[0]['eps_cagr_5yr']:.2f}%"
        if pd.notna(company.iloc[0]["eps_cagr_5yr"])
        else "N/A"
    )

    c4.metric(
        "ROCE",
        f"{company.iloc[0]['roce_pct']:.2f}%"
        if pd.notna(company.iloc[0]["roce_pct"])
        else "N/A"
    )

st.divider()

# -----------------------------
# Peer Group Distribution
# -----------------------------
peer_counts = (
    peers.groupby("peer_group_name")
    .size()
    .reset_index(name="Companies")
)

fig = px.bar(
    peer_counts,
    x="peer_group_name",
    y="Companies",
    title="Companies in Each Peer Group",
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------
# Metrics Table
# -----------------------------
st.subheader("Financial Metrics")

st.dataframe(metrics, use_container_width=True)
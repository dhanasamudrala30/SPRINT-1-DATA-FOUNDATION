import streamlit as st
import plotly.express as px

from utils.db import get_companies, get_ratios

st.title(" Trend Analysis")

# -----------------------------
# Load Data
# -----------------------------
companies = get_companies()
ratios = get_ratios()

# -----------------------------
# Company Selection
# -----------------------------
selected_company = st.selectbox(
    "Select Company",
    companies
)

company_df = ratios[
    ratios["company_id"] == selected_company
].sort_values("year")

if company_df.empty:
    st.warning("No data available.")
    st.stop()

# -----------------------------
# Metric Selection
# -----------------------------
metrics = [
    "net_profit_margin_pct",
    "book_value_per_share",
    "dividend_payout_ratio_pct",
    "total_debt_cr",
    "cash_from_operations_cr"
]

selected_metric = st.selectbox(
    "Select Metric",
    metrics
)

fig = px.line(
    company_df,
    x="year",
    y=selected_metric,
    markers=True,
    title=f"{selected_company} - {selected_metric}"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Underlying Data")
st.dataframe(company_df, use_container_width=True)
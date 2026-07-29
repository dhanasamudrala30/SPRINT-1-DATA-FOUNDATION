import streamlit as st
import plotly.express as px

from utils.db import get_companies, get_ratios

st.title(" Company Profile")

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
# Latest Financial Snapshot
# -----------------------------
latest = company_df.iloc[-1]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Net Profit Margin",
    f"{latest['net_profit_margin_pct']:.2f}%"
)

c2.metric(
    "Book Value / Share",
    f"{latest['book_value_per_share']:.2f}"
)

c3.metric(
    "Dividend Payout",
    f"{latest['dividend_payout_ratio_pct']:.2f}%"
)

c4.metric(
    "Total Debt",
    f"{latest['total_debt_cr']:.2f}"
)

st.divider()

# -----------------------------
# Trend Chart
# -----------------------------
st.subheader("Net Profit Margin Trend")

fig = px.line(
    company_df,
    x="year",
    y="net_profit_margin_pct",
    markers=True,
    title=f"{selected_company} Net Profit Margin"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------
# Financial Data
# -----------------------------
st.subheader("Financial Ratios")

st.dataframe(
    company_df,
    use_container_width=True
)

# -----------------------------
# Download CSV
# -----------------------------
csv = company_df.to_csv(index=False).encode("utf-8")

st.download_button(
    " Download Company Data",
    csv,
    file_name=f"{selected_company}_financial_ratios.csv",
    mime="text/csv"
)
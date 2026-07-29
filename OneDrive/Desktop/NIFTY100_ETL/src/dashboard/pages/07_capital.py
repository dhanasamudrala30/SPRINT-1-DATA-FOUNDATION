import streamlit as st
import plotly.express as px

from utils.db import get_companies, get_ratios

st.title(" Capital Allocation")

companies = get_companies()
ratios = get_ratios()

selected_company = st.selectbox(
    "Select Company",
    companies
)

company = ratios[
    ratios["company_id"] == selected_company
].sort_values("year")

if company.empty:
    st.warning("No data available.")
    st.stop()

fig = px.line(
    company,
    x="year",
    y=[
        "total_debt_cr",
        "cash_from_operations_cr"
    ],
    markers=True,
    title=f"{selected_company} Capital Allocation"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Financial Data")

st.dataframe(company, use_container_width=True)
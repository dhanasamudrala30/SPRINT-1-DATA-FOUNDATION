import streamlit as st
import pandas as pd
from pathlib import Path

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="NIFTY100 Financial Dashboard",
    page_icon="📈",
    layout="wide"
)

# ----------------------------
# Paths
# ----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RATIOS = PROJECT_ROOT / "data" / "processed" / "financial_ratios.csv"
METRICS = PROJECT_ROOT / "data" / "processed" / "financial_metrics.csv"
PEERS = PROJECT_ROOT / "data" / "processed" / "peer_groups.csv"

# ----------------------------
# Load Data
# ----------------------------
ratios = pd.read_csv(RATIOS)
metrics = pd.read_csv(METRICS)
peers = pd.read_csv(PEERS)

# Latest financial year
ratios = (
    ratios.sort_values("year")
          .groupby("company_id", as_index=False)
          .tail(1)
)

# Merge datasets
df = (
    ratios
    .merge(metrics, on="company_id", how="left")
    .merge(peers[["company_id", "peer_group_name"]], on="company_id", how="left")
)

# ----------------------------
# Dashboard Title
# ----------------------------
st.title("📈 NIFTY100 Financial Dashboard")

st.markdown("---")

# ----------------------------
# Company Selector
# ----------------------------
company = st.selectbox(
    "Select Company",
    sorted(df["company_id"].unique())
)

company_data = df[df["company_id"] == company].iloc[0]

st.success(f"Showing financial data for **{company}**")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "ROE (%)",
    f"{company_data['return_on_equity_pct']:.2f}"
)

col2.metric(
    "ROCE (%)",
    f"{company_data['roce_pct']:.2f}"
)

col3.metric(
    "Net Profit Margin (%)",
    f"{company_data['net_profit_margin_pct']:.2f}"
)

col4.metric(
    "Debt / Equity",
    f"{company_data['debt_to_equity']:.2f}"
)

st.markdown("---")

st.subheader("📊 Financial Radar Chart")

RADAR_DIR = PROJECT_ROOT / "reports" / "radar_charts"

radar_file = RADAR_DIR / f"{company}_radar.png"

if radar_file.exists():
    st.image(str(radar_file), use_container_width=True)
else:
    st.warning("Radar chart not found for this company.")

st.markdown("---")

st.subheader("📋 Financial Metrics")

display_columns = [
    "return_on_equity_pct",
    "roce_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr"
]

st.dataframe(
    company_data[display_columns].to_frame(name="Value"),
    use_container_width=True
)

st.markdown("---")

st.subheader("👥 Peer Group")

st.write(f"**Peer Group:** {company_data['peer_group_name']}")

peer_companies = df[
    df["peer_group_name"] == company_data["peer_group_name"]
]["company_id"].tolist()

st.write(peer_companies)

total_companies = df["company_id"].nunique()
total_peer_groups = df["peer_group_name"].nunique()
avg_roe = df["return_on_equity_pct"].mean()
avg_roce = df["roce_pct"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Companies", total_companies)
c2.metric("Peer Groups", total_peer_groups)
c3.metric("Average ROE", f"{avg_roe:.2f}%")
c4.metric("Average ROCE", f"{avg_roce:.2f}%")

st.sidebar.title("Dashboard Filters")

selected_peer = st.sidebar.selectbox(
    "Select Peer Group",
    ["All"] + sorted(df["peer_group_name"].dropna().unique().tolist())
)

if selected_peer != "All":
    df = df[df["peer_group_name"] == selected_peer]

st.markdown("---")
st.subheader("📄 Dataset Preview")

st.dataframe(df, use_container_width=True)
csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Processed Data",
    data=csv,
    file_name="financial_dashboard.csv",
    mime="text/csv"
)



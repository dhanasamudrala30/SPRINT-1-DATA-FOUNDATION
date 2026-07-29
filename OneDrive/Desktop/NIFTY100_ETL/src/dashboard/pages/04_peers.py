import streamlit as st
from pathlib import Path

from utils.db import (
    get_companies,
    get_peers,
    get_peer_percentiles
)

st.title(" Peer Comparison")

# -------------------------------------------------
# Load Data
# -------------------------------------------------
companies = get_companies()
peer_groups = get_peers()
peer_percentiles = get_peer_percentiles()

# -------------------------------------------------
# Company Selection
# -------------------------------------------------
selected_company = st.selectbox(
    "Select Company",
    companies
)

# -------------------------------------------------
# Find Peer Group
# -------------------------------------------------
peer_info = peer_groups[
    peer_groups["company_id"] == selected_company
]

if peer_info.empty:
    st.warning("No peer group found for this company.")
    st.stop()

peer_group = peer_info.iloc[0]["peer_group_name"]

st.success(f" Peer Group: {peer_group}")

# -------------------------------------------------
# Peer Companies
# -------------------------------------------------
st.subheader("Companies in the Peer Group")

group_df = peer_groups[
    peer_groups["peer_group_name"] == peer_group
]

st.dataframe(group_df, use_container_width=True)

# -------------------------------------------------
# Benchmark Company
# -------------------------------------------------
benchmark = group_df[group_df["is_benchmark"] == True]

if not benchmark.empty:
    st.info(f" Benchmark Company: {benchmark.iloc[0]['company_id']}")

# -------------------------------------------------
# Peer Percentile Rankings
# -------------------------------------------------
st.subheader("Peer Percentile Rankings")

company_percentile = peer_percentiles[
    peer_percentiles["company_id"] == selected_company
]

if company_percentile.empty:
    st.warning("No percentile data available.")
else:
    st.dataframe(
        company_percentile,
        use_container_width=True
    )

# -------------------------------------------------
# Radar Chart
# -------------------------------------------------
st.subheader(" Radar Chart")

PROJECT_ROOT = Path(__file__).resolve().parents[3]

chart_folder = PROJECT_ROOT / "reports" / "radar_charts"

# Your files are named like TCS_radar.png
chart_path = chart_folder / f"{selected_company}_radar.png"

if chart_path.exists():

    st.image(
        str(chart_path),
        caption=f"{selected_company} Radar Chart",
        use_container_width=True
    )

else:

    st.error(f"Radar chart not found for {selected_company}")

    # Helpful debugging information
    st.write("Expected file:")
    st.code(str(chart_path))

    if chart_folder.exists():
        st.write("Available radar charts:")
        st.write(sorted([f.name for f in chart_folder.glob("*.png")]))
    else:
        st.error("Radar chart folder does not exist.")
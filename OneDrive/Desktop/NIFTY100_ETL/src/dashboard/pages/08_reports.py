import streamlit as st

from utils.db import (
    get_metrics,
    get_ratios,
    get_peers
)

st.title(" Reports")

metrics = get_metrics()
ratios = get_ratios()
peers = get_peers()

st.subheader("Download Reports")

st.download_button(
    " Financial Metrics",
    metrics.to_csv(index=False).encode("utf-8"),
    "financial_metrics.csv",
    "text/csv"
)

st.download_button(
    " Financial Ratios",
    ratios.to_csv(index=False).encode("utf-8"),
    "financial_ratios.csv",
    "text/csv"
)

st.download_button(
    " Peer Groups",
    peers.to_csv(index=False).encode("utf-8"),
    "peer_groups.csv",
    "text/csv"
)

st.success("Reports are ready for download.")
import streamlit as st
import plotly.express as px

from utils.db import get_peers

st.title(" Sector Analysis")

peers = get_peers()

sector_summary = (
    peers.groupby("peer_group_name")
    .size()
    .reset_index(name="Companies")
)

st.subheader("Companies by Peer Group")

fig = px.bar(
    sector_summary,
    x="peer_group_name",
    y="Companies",
    text="Companies",
    title="Peer Group Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Peer Group Data")

st.dataframe(peers, use_container_width=True)
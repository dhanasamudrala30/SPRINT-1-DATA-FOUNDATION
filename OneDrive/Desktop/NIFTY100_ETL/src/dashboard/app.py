import streamlit as st

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Nifty 100 Analytics",
    # page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Main Title
# --------------------------------------------------
st.title(" Nifty 100 Analytics Dashboard")

st.markdown(
    """
    Welcome to the **Nifty 100 Analytics Dashboard**.

    This application provides financial analytics, screening, peer comparison,
    valuation insights, and interactive visualizations for Nifty 100 companies.

    **Use the sidebar to navigate between the available dashboard pages.**
    """
)

st.markdown("---")

# --------------------------------------------------
# Sprint Information
# --------------------------------------------------
st.subheader("Sprint 4 - Dashboard & Valuation Module")

st.success(" Dashboard scaffold initialized successfully.")

st.write("### Available Screens")

screens = [
    " Home",
    " Company Profile",
    " Financial Screener",
    " Peer Comparison",
    " Trend Analysis",
    " Sector Analysis",
    " Capital Allocation",
    " Annual Reports"
]

for screen in screens:
    st.write(f"- {screen}")

st.markdown("---")

st.info(
    "The dashboard pages will automatically appear in the sidebar once the "
    "`pages/` directory is created and populated."
)


st.markdown("---")
st.caption(
    "NIFTY100 Analytics Dashboard | Bluestock Internship Project | Built with Streamlit"
)
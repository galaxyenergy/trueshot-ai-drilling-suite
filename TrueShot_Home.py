import streamlit as st

st.set_page_config(
    page_title="TrueShot AI Drilling Intelligence Suite",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 TrueShot AI Drilling Intelligence Suite")

st.markdown("""
### AI-Powered Drilling Intelligence Platform

Applications available:

- MWD Predictive Maintenance
- Directional Drilling Analytics
- ROP Optimization
- Anti-Collision Monitoring
- Torque & Drag Analytics
- Hydraulic Optimization
- Automated Reporting

Select a module from the sidebar.
""")

st.image("assets/trueshot_logo.png", width=300)

st.divider()

st.caption(
    "TrueShot LLC | AI-Powered Drilling Intelligence Platform | Tony Lawal"
)
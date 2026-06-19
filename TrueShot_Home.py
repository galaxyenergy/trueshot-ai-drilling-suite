import streamlit as st

st.set_page_config(
    page_title="TrueShot AI Drilling Intelligence Suite",
    page_icon="🚀",
    layout="wide"
)

# Executive Dashboard KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Active Wells", "3")

with col2:
    st.metric("MWD Health", "92%")

with col3:
    st.metric("Average ROP", "84 ft/hr")

with col4:
    st.metric("Collision Alerts", "0")



st.title("🚀 Galaxy AI Drilling Operations Platform")
st.subheader("Client Demonstration: TRUEshot LLC")

st.markdown("""
### Executive Dashboard

Integrated AI-powered drilling analytics platform for:

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
    "Galaxy AI Drilling Operations Platform | TRUEshot LLC Demonstration | Tony Lawal 2026"
)
import streamlit as st

from login import login_screen

st.success("LOGIN MODULE IMPORTED")

st.set_page_config(
    page_title="Galaxy AI Drilling Intelligence Suite Powered by TRUEshot Data",
    page_icon="🚀",
    layout="wide"
)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_screen()
    st.stop()
    

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


col_title, col_logo = st.columns([4,1])

with col_title:
    st.markdown("""
<h1 style='font-size:40px;'>
🚀 Galaxy AI Drilling Operations Platform
</h1>
""", unsafe_allow_html=True)
    st.info("🏢 Client Demonstration: TRUEshot LLC")

with col_logo:
    st.image("assets/trueshot_logo.png", width=220)


st.markdown("""
### Executive Dashboard

Unified AI Platform for Drilling Optimization, Predictive Maintenance, and Operational Excellence
""")


st.subheader("AI Drilling Applications")

row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    st.success("🛠 Predictive Maintenance")

with row1_col2:
    st.success("🧭 Directional Analytics")

with row1_col3:
    st.success("📈 ROP Optimization")

row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.warning("⚠️ Anti-Collision")

with row2_col2:
    st.info("🔩 Torque & Drag")

with row2_col3:
    st.info("🌊 Hydraulics")

st.success("📄 Automated Reporting")


st.write("Select a module from the sidebar.")

st.divider()

st.caption(
    "Galaxy AI Drilling Operations Platform | TRUEshot LLC Demonstration | Tony Lawal 2026"
)

st.sidebar.divider()

if st.sidebar.button("Logout"):

    st.session_state["authenticated"] = False
    st.rerun()
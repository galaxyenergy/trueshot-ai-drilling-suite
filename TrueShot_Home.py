import streamlit as st
import pandas as pd
import numpy as np
from services.shift_analysis_service import build_current_shift_analysis
from login import login_screen


#st.success("LOGIN MODULE IMPORTED")

st.set_page_config(
    page_title="Galaxy AI Drilling Intelligence Suite Powered by TrueShot Data",
    page_icon="🚀",
    layout="wide"
)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_screen()
    st.stop()
    

# ==================================================
# HOME PAGE KPI CARDS - DYNAMIC FROM OPERATIONS DATA CENTER
# ==================================================

analysis = build_current_shift_analysis()
standard_df = st.session_state.get("standard_df")

active_wells = 0
mwd_health_text = "N/A"
avg_rop_text = "N/A"
collision_alerts = "N/A"

if analysis is not None:
    metrics = analysis["metrics"]
    active_wells = 1
    avg_rop_text = f"{metrics.get('avg_rop', 0):,.1f} ft/hr"

if standard_df is not None and not standard_df.empty:
    health_score = 100

    if "Battery" in standard_df.columns:
        battery = pd.to_numeric(standard_df["Battery"], errors="coerce")
        battery = battery.replace([-999.25, -999, -9999, -99999], np.nan)
        valid_battery = battery[battery > 0]

        if len(valid_battery) > 0:
            min_battery = valid_battery.tail(100).min()

            if min_battery < 20:
                health_score -= 40
            elif min_battery < 40:
                health_score -= 20

    if "Pulse_Quality" in standard_df.columns:
        pulse = pd.to_numeric(standard_df["Pulse_Quality"], errors="coerce")
        pulse = pulse.replace([-999.25, -999, -9999, -99999], np.nan)
        valid_pulse = pulse[pulse > 0]

        if len(valid_pulse) > 0:
            avg_pulse = valid_pulse.tail(100).mean()

            if avg_pulse < 60:
                health_score -= 30
            elif avg_pulse < 80:
                health_score -= 15

    mwd_health_text = f"{max(0, min(100, health_score)):.0f}%"

    if "Distance" in standard_df.columns:
        distance = pd.to_numeric(standard_df["Distance"], errors="coerce")
        distance = distance.replace([-999.25, -999, -9999, -99999], np.nan)
        collision_alerts = int((distance < 1200).sum())

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Active Wells", active_wells)

with col2:
    st.metric("MWD Health", mwd_health_text)

with col3:
    st.metric("Average ROP", avg_rop_text)

with col4:
    st.metric("Collision Alerts", collision_alerts)



col_title, col_logo = st.columns([4,1])

with col_title:
    st.markdown("""
<h1 style='font-size:40px;'>
🚀 Galaxy AI Drilling Operations Platform
</h1>
""", unsafe_allow_html=True)
    st.info("🏢 Client Demonstration: TrueShot LLC")

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
    "Galaxy AI Drilling Operations Platform | TrueShot LLC Demonstration | Tony Lawal 2026"
)

st.sidebar.divider()

if st.sidebar.button("Logout"):

    st.session_state["authenticated"] = False
    st.rerun()
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.auth_guard import require_login
from utils.datasource import get_module_data
from services.shift_analysis_service import build_current_shift_analysis

require_login()


st.title("🌊 Hydraulics Optimization")

# ==================================================
# HYDRAULICS ANALYSIS FROM OPERATIONS DATA CENTER
# ==================================================

df = get_module_data("hydraulics_df")

if df is None or df.empty:
    st.warning("Please import a WellData export in Operations Data Center.")
    st.stop()

st.session_state["hydraulics_df"] = df

analysis = build_current_shift_analysis()

if analysis is None:
    st.warning("Please import a WellData export in Operations Data Center.")
    st.stop()

metrics = analysis["metrics"]
shift_df = analysis["shift_df"].copy()

# Make sure required columns exist
required_cols = ["Depth", "SPP", "ECD", "FlowRate"]

for col in required_cols:
    if col not in shift_df.columns:
        st.warning(f"{col} column is missing from the standardized WellData export.")
        st.stop()

# Prepare chart dataframe
plot_df = shift_df[["Depth", "SPP", "ECD", "FlowRate"]].copy()

for col in plot_df.columns:
    plot_df[col] = pd.to_numeric(plot_df[col], errors="coerce").fillna(0)

plot_df = plot_df.sort_values("Depth")

# ==================================================
# KPI CARDS
# ==================================================

st.subheader("12-Hour Hydraulics Performance Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current SPP",
        f"{metrics['current_spp']:,.1f} psi"
    )

with col2:
    st.metric(
        "Average SPP",
        f"{metrics['avg_spp']:,.1f} psi"
    )

with col3:
    st.metric(
        "Current ECD",
        f"{metrics['current_ecd']:,.2f} ppg"
    )

with col4:
    st.metric(
        "Average Flow Rate",
        f"{metrics['avg_flowrate']:,.1f}"
    )

# ==================================================
# CHARTS
# ==================================================

st.subheader("Standpipe Pressure vs Depth — Last 12 Hours")

fig_spp = px.line(
    plot_df,
    x="Depth",
    y="SPP",
    title="Standpipe Pressure vs Depth — Last 12 Hours"
)

st.plotly_chart(fig_spp, use_container_width=True)

st.subheader("ECD vs Depth — Last 12 Hours")

fig_ecd = px.line(
    plot_df,
    x="Depth",
    y="ECD",
    title="ECD vs Depth — Last 12 Hours"
)

st.plotly_chart(fig_ecd, use_container_width=True)

st.subheader("Flow Rate vs Depth — Last 12 Hours")

fig_flow = px.line(
    plot_df,
    x="Depth",
    y="FlowRate",
    title="Flow Rate vs Depth — Last 12 Hours"
)

st.plotly_chart(fig_flow, use_container_width=True)

# ==================================================
# AI HYDRAULICS EVALUATION
# ==================================================

st.subheader("AI Hydraulics Evaluation")

current_spp = metrics["current_spp"]
avg_spp = metrics["avg_spp"]
current_ecd = metrics["current_ecd"]
avg_ecd = metrics["avg_ecd"]
avg_flowrate = metrics["avg_flowrate"]
avg_rop = metrics["avg_rop"]
npt_hours = metrics["npt_hours"]

if current_spp <= 0 and current_ecd <= 0:
    ai_message = """
Hydraulics channels were not available or did not contain valid positive values in the evaluated 12-hour window.

Recommendation:
Confirm that standpipe pressure, ECD, and flow-rate channels are included in the WellData export before using this page for final operations analysis.
"""
elif avg_flowrate <= 0:
    ai_message = f"""
Flow-rate data was unavailable or invalid during the evaluated 12-hour window.

Current SPP: {current_spp:,.1f} psi
Average SPP: {avg_spp:,.1f} psi
Current ECD: {current_ecd:,.2f} ppg
Average ECD: {avg_ecd:,.2f} ppg
Average ROP: {avg_rop:,.1f} ft/hr

AI Evaluation:
Hydraulics interpretation is limited without valid flow-rate data.

Recommendation:
Verify pump output or flow-rate channel mapping from the WellData export. Confirm hole-cleaning performance with SPP trend, ECD behavior, cuttings returns, torque trend, and ROP response.
"""
elif current_ecd > avg_ecd * 1.15 and avg_ecd > 0:
    ai_message = f"""
ECD is elevated compared with the 12-hour average.

Current ECD: {current_ecd:,.2f} ppg
Average ECD: {avg_ecd:,.2f} ppg
Current SPP: {current_spp:,.1f} psi
Average Flow Rate: {avg_flowrate:,.1f}
Estimated NPT: {npt_hours:.1f} hrs

AI Evaluation:
Elevated ECD may indicate increased annular pressure losses, cuttings loading, hole-cleaning issues, flow restrictions, or changing mud/hole conditions.

Recommendation:
Review ECD trend with SPP, flow rate, torque, hook load, and ROP. Confirm whether any pump-rate changes, mud-property changes, or tight-hole symptoms occurred during this interval.
"""
else:
    ai_message = f"""
Hydraulic performance appears stable within the evaluated 12-hour window.

Current SPP: {current_spp:,.1f} psi
Average SPP: {avg_spp:,.1f} psi
Current ECD: {current_ecd:,.2f} ppg
Average ECD: {avg_ecd:,.2f} ppg
Average Flow Rate: {avg_flowrate:,.1f}
Average ROP: {avg_rop:,.1f} ft/hr

AI Evaluation:
No major hydraulic instability was detected from the uploaded 12-hour operational data.

Recommendation:
Continue monitoring SPP, ECD, flow rate, torque, hook load, and ROP. Maintain current hydraulics program unless pressure, ECD, or torque begins trending upward.
"""

st.text_area(
    "AI Hydraulics Recommendation",
    ai_message,
    height=300
)
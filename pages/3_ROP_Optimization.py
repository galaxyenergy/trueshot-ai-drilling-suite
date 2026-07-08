import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.auth_guard import require_login
from utils.datasource import get_module_data
from services.shift_analysis_service import build_current_shift_analysis


st.set_page_config(
    page_title="ROP Optimization",
    page_icon="⚡",
    layout="wide"
)

require_login()


df = get_module_data("rop_df")

if df is None or df.empty:
    st.warning("Please import a WellData export in Operations Data Center.")
    st.stop()

st.session_state["rop_df"] = df




st.title("⚡ ROP Optimization")
st.caption("Rate of Penetration analytics and drilling performance monitoring")

# ==================================================
# AI 12-HOUR ROP ANALYSIS FROM OPERATIONS DATA CENTER
# ==================================================

analysis = build_current_shift_analysis()

if analysis is None:
    st.warning("Please import a WellData export in Operations Data Center.")
    st.stop()

metrics = analysis["metrics"]
shift_df = analysis["shift_df"].copy()

# Make sure required ROP columns exist
if "Depth" not in shift_df.columns or "ROP" not in shift_df.columns:
    st.warning("Depth or ROP column is missing from the standardized WellData export.")
    st.stop()

# Clean chart data
plot_df = shift_df[["Depth", "ROP"]].copy()
plot_df["Depth"] = pd.to_numeric(plot_df["Depth"], errors="coerce").fillna(0)
plot_df["ROP"] = pd.to_numeric(plot_df["ROP"], errors="coerce").fillna(0)
plot_df = plot_df.sort_values("Depth")

rop_positive = plot_df["ROP"][plot_df["ROP"] > 0]

current_rop = metrics.get("current_rop", plot_df["ROP"].iloc[-1] if len(plot_df) else 0)
avg_rop = metrics.get("avg_rop", rop_positive.mean() if len(rop_positive) else 0)
max_rop = rop_positive.max() if len(rop_positive) else 0
min_rop = rop_positive.min() if len(rop_positive) else 0
footage_drilled = metrics.get("footage_drilled", 0)
npt_hours = metrics.get("npt_hours", 0)

# ==================================================
# KPI CARDS
# ==================================================

st.subheader("12-Hour ROP Performance Summary")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Current ROP",
        f"{current_rop:,.1f} ft/hr"
    )

with col2:
    st.metric(
        "Average ROP",
        f"{avg_rop:,.1f} ft/hr"
    )

with col3:
    st.metric(
        "Best ROP",
        f"{max_rop:,.1f} ft/hr"
    )

with col4:
    st.metric(
        "Footage Drilled",
        f"{footage_drilled:,.1f} ft"
    )
    
with col5:
    st.metric(
        "Current Hole Depth",
        f"{metrics.get('current_hole_depth', 0):,.1f} ft"
)    

# ==================================================
# ROP CHARTS
# ==================================================

st.subheader("ROP vs Depth — Last 12 Hours")

fig_rop = px.line(
    plot_df,
    x="Depth",
    y="ROP",
    title="Rate of Penetration vs Depth — Last 12 Hours"
)

st.plotly_chart(
    fig_rop,
    use_container_width=True
)

plot_df["rop_avg"] = plot_df["ROP"].rolling(10).mean()

st.subheader("ROP Trend — Rolling Average")

fig_avg = px.line(
    plot_df,
    x="Depth",
    y="rop_avg",
    title="Rolling Average ROP — Last 12 Hours"
)

st.plotly_chart(
    fig_avg,
    use_container_width=True
)

# ==================================================
# FORMATION PERFORMANCE
# ==================================================

zone_labels = []

for md in plot_df["Depth"]:
    if md < 5000:
        zone_labels.append("Surface")
    elif md < 10000:
        zone_labels.append("Intermediate")
    elif md < 15000:
        zone_labels.append("Curve")
    else:
        zone_labels.append("Lateral")

plot_df["Zone"] = zone_labels

zone_perf = (
    plot_df.groupby("Zone")["ROP"]
    .mean()
    .reset_index()
    .rename(columns={"ROP": "Average ROP (ft/hr)"})
)

zone_order = [
    "Surface",
    "Intermediate",
    "Curve",
    "Lateral"
]

zone_perf["Zone"] = pd.Categorical(
    zone_perf["Zone"],
    categories=zone_order,
    ordered=True
)

zone_perf = zone_perf.sort_values("Zone")
zone_perf["Average ROP (ft/hr)"] = zone_perf["Average ROP (ft/hr)"].round(1)

st.subheader("Formation / Hole Section Performance")

st.dataframe(
    zone_perf,
    hide_index=True,
    use_container_width=True
)

# ==================================================
# AI ROP INSIGHTS
# ==================================================

st.subheader("AI ROP Evaluation")

if avg_rop <= 0:
    ai_message = """
No valid positive ROP was detected in the evaluated 12-hour window.

Recommendation:
Confirm the ROP channel, depth movement, and drilling activity records. If the rig was drilling, review whether the WellData export is using a different ROP channel name.
"""
elif current_rop < avg_rop * 0.8:
    ai_message = f"""
Current ROP is below the 12-hour average.

Current ROP: {current_rop:,.1f} ft/hr
Average ROP: {avg_rop:,.1f} ft/hr
Best ROP: {max_rop:,.1f} ft/hr
Estimated NPT: {npt_hours:.1f} hrs

Recommendation:
Investigate bit condition, formation change, WOB transfer, RPM, torque response, hydraulics, and possible cleaning issues. Compare this interval against torque, SPP, ECD, and flow-rate behavior before changing parameters.
"""
else:
    ai_message = f"""
ROP is operating within the expected 12-hour performance range.

Current ROP: {current_rop:,.1f} ft/hr
Average ROP: {avg_rop:,.1f} ft/hr
Best ROP: {max_rop:,.1f} ft/hr
Footage Drilled: {footage_drilled:,.1f} ft
Current Hole Depth: {current_hole_depth:, 0:,.1f} ft

Recommendation:
Continue monitoring ROP together with torque, RPM, SPP, ECD, flow rate, and hook load. Maintain current drilling parameters unless torque, hydraulics, or hole-cleaning indicators begin to deteriorate.
"""

st.text_area(
    "AI ROP Recommendation",
    ai_message,
    height=260
)
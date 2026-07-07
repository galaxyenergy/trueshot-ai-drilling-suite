import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime
from utils.auth_guard import require_login
from utils.datasource import get_module_data
from services.shift_analysis_service import build_current_shift_analysis


st.set_page_config(
    page_title="TrueShot AI - Torque & Drag",
    page_icon="🔩",
    layout="wide"
)

require_login()

dataset = st.session_state.get("current_dataset")


st.title("🔩 Torque & Drag Analytics")

# ==================================================
# ANTI-COLLISION ANALYSIS FROM OPERATIONS DATA CENTER
# ==================================================

df = get_module_data("anti_collision_df")

if df is None or df.empty:
    st.warning("Please import a WellData export in Operations Data Center.")
    st.stop()

st.session_state["anti_collision_df"] = df
st.session_state["collision_df"] = df
st.session_state["survey_df"] = df

analysis = build_current_shift_analysis()

if analysis is None:
    st.warning("Please import a WellData export in Operations Data Center.")
    st.stop()

metrics = analysis["metrics"]
shift_df = analysis["shift_df"].copy()

# Make sure required columns exist
if "Depth" not in shift_df.columns:
    st.warning("Depth column is missing from the standardized WellData export.")
    st.stop()

if "Distance" not in shift_df.columns:
    shift_df["Distance"] = 1500

# Prepare chart dataframe
plot_df = shift_df[["Depth", "Distance"]].copy()

plot_df["Depth"] = pd.to_numeric(plot_df["Depth"], errors="coerce").fillna(0)
plot_df["Distance"] = pd.to_numeric(plot_df["Distance"], errors="coerce").fillna(1500)

plot_df = plot_df.sort_values("Depth")

# Detect whether real offset separation data exists
has_dynamic_offset_data = plot_df["Distance"].nunique() > 1

minimum_distance = plot_df["Distance"].min()
average_distance = plot_df["Distance"].mean()
collision_alerts = int((plot_df["Distance"] < 1200).sum())
critical_alerts = int((plot_df["Distance"] < 800).sum())

# ==================================================
# KPI CARDS
# ==================================================

st.subheader("12-Hour Anti-Collision Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Minimum Separation",
        f"{minimum_distance:,.1f} ft"
    )

with col2:
    st.metric(
        "Average Separation",
        f"{average_distance:,.1f} ft"
    )

with col3:
    st.metric(
        "Warning Alerts",
        f"{collision_alerts}"
    )

with col4:
    st.metric(
        "Critical Alerts",
        f"{critical_alerts}"
    )

# ==================================================
# CHART
# ==================================================

st.subheader("Separation Distance vs Depth — Last 12 Hours")

fig_distance = px.line(
    plot_df,
    x="Depth",
    y="Distance",
    title="Offset Well Separation vs Depth — Last 12 Hours"
)

fig_distance.add_hline(
    y=1200,
    line_dash="dash",
    annotation_text="Warning Threshold: 1200 ft"
)

fig_distance.add_hline(
    y=800,
    line_dash="dash",
    annotation_text="Critical Threshold: 800 ft"
)

st.plotly_chart(fig_distance, use_container_width=True)

# ==================================================
# RISK TABLE
# ==================================================

risk_df = plot_df.tail(50).copy()

def classify_risk(distance):
    if distance < 800:
        return "Critical"
    elif distance < 1200:
        return "Warning"
    return "Low"

risk_df["Risk"] = risk_df["Distance"].apply(classify_risk)

st.subheader("Recent Anti-Collision Risk Table")

st.dataframe(
    risk_df[["Depth", "Distance", "Risk"]],
    use_container_width=True,
    hide_index=True
)

# ==================================================
# AI ANTI-COLLISION EVALUATION
# ==================================================

st.subheader("AI Anti-Collision Evaluation")

if not has_dynamic_offset_data:
    ai_message = f"""
The uploaded WellData export was successfully read from Operations Data Center, but no dynamic offset-well separation data was detected.

Current Status:
Minimum Separation Displayed: {minimum_distance:,.1f} ft
Warning Alerts: {collision_alerts}
Critical Alerts: {critical_alerts}

AI Evaluation:
This page is currently showing a placeholder separation value because the uploaded operational export does not appear to include true offset-well distance, closest approach, or anti-collision separation data.

Important:
A real anti-collision analysis requires at least:
1. Active well survey trajectory
2. Offset well survey trajectory
3. Northing / Easting / TVD or equivalent positional data
4. Separation factor or calculated center-to-center distance

Recommendation:
For the meeting demo, explain that the Operations Data Center can feed the anti-collision module, but true anti-collision validation requires uploading survey and offset-well files. Until those are provided, the system should not claim real collision clearance.
"""
elif critical_alerts > 0:
    ai_message = f"""
Critical anti-collision risk detected in the evaluated 12-hour window.

Minimum Separation: {minimum_distance:,.1f} ft
Critical Alerts: {critical_alerts}
Warning Alerts: {collision_alerts}

AI Evaluation:
Separation distance dropped below the critical threshold. This requires immediate review before continuing directional drilling operations.

Recommendation:
Stop and review active well survey, offset well survey, directional plan, uncertainty model, and separation factor. Confirm whether the distance is true center-to-center separation or a calculated projection before making operational decisions.
"""
elif collision_alerts > 0:
    ai_message = f"""
Anti-collision warning condition detected in the evaluated 12-hour window.

Minimum Separation: {minimum_distance:,.1f} ft
Warning Alerts: {collision_alerts}

AI Evaluation:
Separation distance dropped below the warning threshold but did not reach the critical threshold.

Recommendation:
Review the active well plan, offset well position, latest survey, and projected separation trend. Continue monitoring before drilling ahead.
"""
else:
    ai_message = f"""
No anti-collision warning or critical condition was detected in the evaluated 12-hour window.

Minimum Separation: {minimum_distance:,.1f} ft
Average Separation: {average_distance:,.1f} ft
Warning Alerts: {collision_alerts}
Critical Alerts: {critical_alerts}

AI Evaluation:
Available separation values remained above the warning threshold.

Recommendation:
Continue monitoring separation trend. For final client use, confirm that the distance channel is calculated from valid active-well and offset-well survey data.
"""

st.text_area(
    "AI Anti-Collision Recommendation",
    ai_message,
    height=320
)
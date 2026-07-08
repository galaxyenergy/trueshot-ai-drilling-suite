import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
#import joblib
from utils.auth_guard import require_login


from utils.datasource import get_module_data
from services.shift_analysis_service import build_current_shift_analysis


st.set_page_config(
    page_title="MWD Predictive Maintenance",
    page_icon="🔧",
    layout="wide"
)



df = get_module_data("mwd_df")

if df is None or df.empty:
    st.warning("Please import a WellData export in Operations Data Center.")
    st.stop()

st.session_state["mwd_df"] = df

analysis = build_current_shift_analysis()

if analysis is None:
    st.warning("Please import a WellData export in Operations Data Center.")
    st.stop()

metrics = analysis["metrics"]
shift_df = analysis["shift_df"]


require_login()

   
   
#st.write(df.columns.tolist())
#st.stop()

current_depth = df["Depth"].iloc[-1]
current_shock = df["Shock"].iloc[-1]
current_vibration = df["Vibration"].iloc[-1]
current_temp = df["Temp"].iloc[-1]
current_pressure = df["Pressure"].iloc[-1]
current_gamma = df["Gamma"].iloc[-1]
current_battery = df["Battery"].iloc[-1]
current_pulse = df["Pulse_Quality"].iloc[-1]
current_rpm = df["RPM"].iloc[-1]
current_wob = df["WOB"].iloc[-1]
current_mudflow = df["Mud_Flow"].iloc[-1]
current_torque = df["Torque"].iloc[-1]

failure_events = df["Failure_Flag"].sum()

health_score = max(
    0,
    100 - current_shock * 0.3 - current_vibration * 3
)

failure_probability = 100 - health_score

prediction = (
    "FAILURE RISK"
    if failure_probability > 40
    else "HEALTHY"
)

importance_df = pd.read_csv(
    "models/mwd/feature_importance.csv"
)

st.caption(
    "AI-powered tool health monitoring and failure prediction"
)

# Prediction

#probability = model.predict_proba(input_data)[0][1]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Footage Drilled",
        f"{metrics['footage_drilled']:,.1f} ft"
    )
with col2:
    st.metric(
        "Current Hole Depth",
        f"{metrics.get('current_hole_depth', 0):,.1f} ft"
    )

with col3:
    st.metric(
        "Average ROP",
        f"{metrics['avg_rop']:,.1f} ft/hr"
    )

with col4:
    st.metric(
        "Average Torque",
        f"{metrics['avg_torque']:,.1f}"
    )

with col5:
    st.metric(
        "Estimated NPT",
        f"{metrics['npt_hours']:.1f} hrs"
    )




st.subheader("Live Tool Health Dashboard")

st.metric("Shock (g)", round(current_shock,2))
st.progress(min(current_shock/10,1.0))

st.metric("Vibration RMS", round(current_vibration,2))
st.progress(min(current_vibration/10,1.0))

st.metric("Temperature (F)", round(current_temp,1))
st.progress(min(current_temp/250,1.0))

st.metric("Battery Voltage", round(current_battery,1))
st.progress(min(current_battery/35,1.0))

st.metric("Pulse Quality", round(current_pulse,1))
st.progress(min(current_pulse/100,1.0))

st.metric("Mud Flow Rate", round(current_mudflow,1))
st.progress(min(current_mudflow/800,1.0))

st.metric("RPM", round(current_rpm,1))
st.progress(min(current_rpm/250,1.0))

st.metric("WOB", round(current_wob,1))
st.progress(min(current_wob/50000,1.0))

st.metric("Torque", round(current_torque,1))
st.progress(min(current_torque/40000,1.0))

# Traffic Light Status

if health_score >= 85:
    st.success("🟢 Tool Status: Excellent")

elif health_score >= 70:
    st.info("🔵 Tool Status: Normal")

elif health_score >= 60:
    st.warning("🟡 Tool Status: Monitor Closely")

else:
    st.error("🔴 Tool Status: Failure Likely")

# Root Cause Analysis

st.subheader("Root Cause Analysis")

st.subheader("Top Risk Drivers")

risk_df = pd.DataFrame({
    "Feature":[
        "Shock",
        "Vibration",
        "Temperature",
        "Pulse Quality",
        "Battery"
    ],
    "Value":[
        current_shock,
        current_vibration,
        current_temp,
        current_pulse,
        current_battery
    ]
})

st.dataframe(
    risk_df,
    width="stretch"
)

st.bar_chart(
    risk_df.set_index("Feature")
)

issues = []

if current_shock > 80:
    issues.append("⚠️ Excessive Shock")

if current_vibration > 7:
    issues.append("⚠️ Excessive Vibration")

if current_temp > 180:
    issues.append("⚠️ High Temperature")

if current_battery < 27:
    issues.append("⚠️ Low Battery Voltage")

if current_pulse < 75:
    issues.append("⚠️ Poor Pulse Quality")

if len(issues) == 0:
    st.success(
        "No critical issues detected. "
        "All monitored parameters are within normal operating limits."
    )
else:
    for issue in issues:
        st.warning(issue)

st.subheader("Shock vs Depth")

fig = px.line(
    df,
    x="Depth",
    y="Shock"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.subheader("Vibration vs Depth")

fig = px.line(
    df,
    x="Depth",
    y="Vibration"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.subheader("Temperature vs Depth")

fig = px.line(
    df,
    x="Depth",
    y="Temp"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.subheader("Pressure vs Depth")

fig = px.line(
    df,
    x="Depth",
    y="Pressure",
    #title="Pressure vs Depth"
)

st.plotly_chart(fig, width="stretch")

st.subheader("Gamma Ray vs Depth")

fig = px.line(
    df,
    x="Depth",
    y="Gamma",
    #title="Gamma Ray vs Depth"
)

st.plotly_chart(fig, width="stretch")

st.subheader("Battery Voltage")

fig = px.line(
    df,
    x="Depth",
    y="Battery"
)

st.plotly_chart(fig, width="stretch")

st.subheader("Pulse Quality")

fig = px.line(
    df,
    x="Depth",
    y="Pulse_Quality"
)

st.plotly_chart(fig, width="stretch")

st.subheader("Inclination vs Depth")

fig = px.line(
    df,
    x="Depth",
    y="Inclination"
)

st.plotly_chart(
    fig,
    width="stretch",
    key="inclination_chart"
)

st.subheader("Azimuth vs Depth")

fig = px.line(
    df,
    x="Depth",
    y="Azimuth"
)

st.plotly_chart(
    fig,
    width="stretch",
    key="azimuth_chart"
)

st.subheader("Toolface vs Depth")

fig = px.line(
    df,
    x="Depth",
    y="Toolface"
)

st.plotly_chart(
    fig,
    width="stretch",
    key="toolface_chart"
)

st.subheader("Pressure vs Depth")

fig = px.line(
    df,
    x="Depth",
    y="Pressure"
)

st.plotly_chart(
    fig,
    width="stretch",
    key="Pressure_chart"
)

st.subheader("Battery Voltage Trend")

battery_data = df.set_index("Timestamp")["Battery"].tail(500)

battery_range = battery_data.max() - battery_data.min()

st.metric(
    "Battery Stability",
    f"{battery_range:.2f}V"
)

st.line_chart(battery_data)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current", f"{battery_data.iloc[-1]:.2f}V")

with col2:
    st.metric("Minimum", f"{battery_data.min():.2f}V")

with col3:
    st.metric("Maximum", f"{battery_data.max():.2f}V"
)

st.subheader("Pulse Quality Trend")
st.line_chart(
    df.set_index("Timestamp")["Pulse_Quality"].tail(500)
)

st.subheader("Vibration Trend")

st.line_chart(
    df.set_index("Timestamp")["Vibration"].tail(500)
)

from utils.helpers import generate_ai_recommendations

recommendations = generate_ai_recommendations(
    health_score,
    failure_probability,
    current_shock,
    current_vibration,
    current_temp,
    current_battery
)

for rec in recommendations:
    st.info(rec)



st.subheader("AI 12-Hour MWD Operational Evaluation")

st.info(
    "This page is using the standardized WellData export imported through Operations Data Center."
)

st.text_area(
    "AI MWD / Operations Recommendation",
    analysis["report_text"],
    height=300
)
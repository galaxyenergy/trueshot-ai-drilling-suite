import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
#import joblib

st.set_page_config(
    page_title="MWD Predictive Maintenance",
    page_icon="🔧",
    layout="wide"
)

if "mwd_df" not in st.session_state:
    st.warning("Please upload MWD CSV in Data Manager.")
    st.stop()

df = st.session_state["mwd_df"]
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

col1, col2, col3 = st.columns([1,1,1])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current Depth",
        f"{current_depth:,.0f} ft"
    )

with col2:
    st.metric(
        "Tool Health",
        f"{health_score:.1f}%"
    )

with col3:
    st.metric(
        "Failure Risk",
        f"{failure_probability:.1f}%"
    )

with col4:
    st.metric(
        "Prediction",
        prediction
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

if "mwd_df" not in st.session_state:
    st.warning("Please upload MWD CSV in Data Manager.")
    st.stop()

df = st.session_state["mwd_df"]

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

st.subheader("Daily MWD Report Generator")

avg_rop = df["ROP"].mean()
max_rop = df["ROP"].max()

avg_wob = df["WOB"].mean()
avg_rpm = df["RPM"].mean()

avg_torque = df["Torque"].mean()

avg_mudflow = df["Mud_Flow"].mean()

avg_gamma = df["Gamma"].mean()

failure_count = df["Failure_Flag"].sum()


report_text = f"""
MWD DAILY REPORT

Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}

Current Depth: {current_depth:,.0f} ft

DRILLING PERFORMANCE

Average ROP: {avg_rop:.1f} ft/hr
Maximum ROP: {max_rop:.1f} ft/hr

Average WOB: {avg_wob:.0f} lbs
Average RPM: {avg_rpm:.0f}
Average Torque: {avg_torque:.0f}
Average Mud Flow: {avg_mudflow:.0f} gpm

TOOL HEALTH

Health Score: {health_score:.1f}
Failure Risk: {failure_probability:.1f}%

Shock: {current_shock:.1f}
Vibration: {current_vibration:.1f}
Temperature: {current_temp:.1f}
Battery: {current_battery:.1f}
Pulse Quality: {current_pulse:.1f}

FORMATION EVALUATION

Average Gamma: {avg_gamma:.1f}

FAILURE ANALYSIS

Failure Events: {failure_count}

AI RECOMMENDATION

Continue drilling operations.
Monitor vibration and temperature trends.
No critical maintenance actions required.
"""

st.text_area(
    "Generated Daily Report",
    report_text,
    height=500
)

st.download_button(
    label="Download Daily Report",
    data=report_text,
    file_name="MWD_Daily_Report.txt",
    mime="text/plain"
)

#from utils.report_generator import generate_mwd_pdf
    
if st.button("Generate PDF Report"):
    pdf_path = "MWD_Daily_Report.pdf"

    generate_mwd_pdf(
        pdf_path,
        report_text
)

# with open(pdf_path, "rb") as f:
#
#     st.download_button(
#         "Download PDF Report",
#         data=f,
#         file_name="MWD_Daily_Report.pdf",
#         mime="application/pdf"
#     )
    
recommendations = []

if current_temp > 180:
    recommendations.append(
        "High temperature detected. Monitor tool cooling."
    )

if current_vibration > 6:
    recommendations.append(
        "Elevated vibration detected."
    )

if current_pulse < 80:
    recommendations.append(
        "Pulse quality deteriorating."
    )

if not recommendations:
    recommendations.append(
        "All monitored parameters remain within acceptable operating limits."
    )

    st.subheader("AI Recommendations")

for rec in recommendations:
    st.info(rec)      
    #GENERATE END OF WELL REPORTS
    
    max_depth = df["Depth"].max()

    avg_rop = df["ROP"].mean()

    avg_shock = df["Shock"].mean()

    avg_vibration = df["Vibration"].mean()

    avg_temp = df["Temp"].mean()

    avg_battery = df["Battery"].mean()

    avg_pulse = df["Pulse_Quality"].mean()

    failure_count = df["Failure_Flag"].sum()

    reliability = max(
        0,
        100 - failure_count * 2
    )

    eow_report = f"""
TRUEshot End Of Well MWD Report

Maximum Depth:
{max_depth:.0f} ft

Average ROP:
{avg_rop:.1f}

Average Shock:
{avg_shock:.1f}

Average Vibration:
{avg_vibration:.1f}

Average Temperature:
{avg_temp:.1f}

Average Battery:
{avg_battery:.1f}

Average Pulse Quality:
{avg_pulse:.1f}

Failure Events:
{failure_count}

Reliability Score:
{reliability:.1f}%
"""

    st.text_area(
        "End of Well Report",
        eow_report,
        height=500
    )

st.download_button(
        "Download End Of Well Report",
        eow_report,
        file_name="End_of_Well_MWD_Report.txt"
    )

#from utils.report_generator import generate_mwd_pdf


#with open(pdf_path, "rb") as f:
#
#       st.download_button(
#            "Download End Of Well PDF",
#            data=f,
#            file_name="End_Of_Well_Report.pdf",
#            mime="application/pdf"
#        )
        
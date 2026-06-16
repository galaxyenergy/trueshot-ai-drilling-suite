import streamlit as st
import pandas as pd
import joblib

importance_df = pd.read_csv(
    "models/mwd/feature_importance.csv"
)

st.set_page_config(
    page_title="MWD Predictive Maintenance",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 MWD Predictive Maintenance")

st.caption(
    "AI-powered tool health monitoring and failure prediction"
)

model = joblib.load("models/mwd/mwd_rf.pkl")



shock = st.slider("Shock (g)", 0, 120, 50)
vibration = st.slider("Vibration RMS", 0.0, 10.0, 4.0)
temperature = st.slider("Temperature (F)", 100, 250, 175)
battery = st.slider("Battery Voltage", 25.0, 30.0, 28.0)
pulse = st.slider("Pulse Quality", 60, 100, 88)
run_hours = st.slider("Run Hours", 0.0, 100.0, 20.0)
flow = st.slider("Mud Flow Rate", 300, 600, 450)
rpm = st.slider("RPM", 50, 200, 120)
wob = st.slider("WOB", 10000, 40000, 25000)

input_data = pd.DataFrame(
    [[
        run_hours,
        shock,
        vibration,
        temperature,
        battery,
        pulse,
        rpm,
        wob,
        flow
    ]],
    columns=[
        "run_hours",
        "shock_g",
        "vibration_rms",
        "temperature_f",
        "battery_voltage",
        "pulse_quality",
        "rpm",
        "wob",
        "mud_flow_rate"
    ]
)

# Prediction

probability = model.predict_proba(input_data)[0][1]

health_score = int((1 - probability) * 100)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "60-Minute Failure Risk",
        f"{probability*100:.1f}%"
    )

with col2:
    st.metric(
        "Tool Health Score",
        f"{health_score}/100"
    )

# Traffic Light Status

if health_score >= 80:
    st.success("🟢 TOOL STATUS: HEALTHY")

elif health_score >= 60:
    st.warning("🟡 TOOL STATUS: MONITOR")

else:
    st.error("🔴 TOOL STATUS: CRITICAL")


# Root Cause Analysis

st.subheader("Root Cause Analysis")

st.subheader("Top Risk Drivers")

display_df = importance_df.copy()

display_df["feature_display"] = (
    display_df["feature"]
    .str.replace("_", " ")
    .str.title()
)

display_df["importance"] = (
    display_df["importance"] * 100
).round(1)

st.dataframe(
    display_df[["feature_display", "importance"]]
        .rename(columns={
            "feature_display": "Feature",
            "importance": "Importance (%)"
        })
        .head(5),
    use_container_width=True
)

# Add this directly below

chart_df = importance_df.head(4).copy()

chart_df["feature_display"] = (
    chart_df["feature"]
    .str.replace("_", " ")
    .str.title()
)

chart_df = chart_df.set_index("feature_display")

st.bar_chart(chart_df["importance"] * 100)


issues = []

if shock > 80:
    issues.append("⚠ High Shock Levels")

if vibration > 7:
    issues.append("⚠ Excessive Vibration")

if battery < 27:
    issues.append("⚠ Low Battery Voltage")

if pulse < 75:
    issues.append("⚠ Poor Pulse Quality")

if len(issues) == 0:
    st.success(
        "No critical issues detected. "
        "All monitored parameters are within normal operating limits."
    )
else:
    for issue in issues:
        st.warning(issue)

df = pd.read_csv("data/mwd/mwd_degradation_timeseries_v4.csv")

st.subheader("Battery Voltage Trend")

battery_data = df.set_index("timestamp")["battery_voltage"].tail(500)

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
    df.set_index("timestamp")["pulse_quality"].tail(500)
)

st.subheader("Vibration RMS Trend")
st.line_chart(
    df.set_index("timestamp")["vibration_rms"].tail(500)
)
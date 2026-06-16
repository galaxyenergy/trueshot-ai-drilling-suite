import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.set_page_config(
    page_title="TrueShot AI ROP Optimizer",
    layout="wide"
)

st.title("TrueShot AI ROP Optimization Dashboard")

st.caption(
    "AI-Based Drilling Performance Optimization"
)

# ---------------------------------
# Load Model
# ---------------------------------

model = joblib.load(
    "models/rop_rf.pkl"
)

# ---------------------------------
# Inputs
# ---------------------------------

st.subheader("Current Drilling Parameters")

col1, col2 = st.columns(2)

with col1:

    rpm = st.slider(
        "RPM",
        60,
        220,
        120
    )

    wob = st.slider(
        "WOB",
        5000,
        45000,
        25000
    )

    flow = st.slider(
        "Flow Rate",
        300,
        800,
        500
    )

with col2:

    shock = st.slider(
        "Shock (g)",
        0,
        100,
        20
    )

    vibration = st.slider(
        "Vibration RMS",
        0.0,
        10.0,
        4.0
    )

    pulse = st.slider(
        "Pulse Quality",
        60,
        100,
        88
    )

battery = st.slider(
    "Battery Voltage",
    25.0,
    30.0,
    28.0
)

# ---------------------------------
# Prediction
# ---------------------------------

input_data = pd.DataFrame(
    [[
        rpm,
        wob,
        flow,
        shock,
        vibration,
        pulse,
        battery
    ]],
    columns=[
        "rpm",
        "wob",
        "flow_rate",
        "shock_g",
        "vibration_rms",
        "pulse_quality",
        "battery_voltage"
    ]
)

predicted_rop = model.predict(
    input_data
)[0]

# ---------------------------------
# Recommendation Engine
# ---------------------------------

recommended_rpm = min(
    rpm + 20,
    220
)

recommended_wob = min(
    wob + 5000,
    45000
)

recommended_input = pd.DataFrame(
    [[
        recommended_rpm,
        recommended_wob,
        flow,
        shock,
        vibration,
        pulse,
        battery
    ]],
    columns=input_data.columns
)

recommended_rop = model.predict(
    recommended_input
)[0]

improvement = (
    (recommended_rop - predicted_rop)
    / predicted_rop
) * 100

# ---------------------------------
# Results
# ---------------------------------

st.subheader("AI Optimization Results")

col3, col4, col5 = st.columns(3)

with col3:
    st.metric(
        "Predicted ROP",
        f"{predicted_rop:.1f} ft/hr"
    )

with col4:
    st.metric(
        "Optimized ROP",
        f"{recommended_rop:.1f} ft/hr"
    )

with col5:
    st.metric(
        "Potential Gain",
        f"{improvement:.1f}%"
    )

# ---------------------------------
# Recommendations
# ---------------------------------

st.subheader("AI Recommendations")

st.success(
    f"Increase RPM from {rpm} to {recommended_rpm}"
)

st.success(
    f"Increase WOB from {wob:,} to {recommended_wob:,}"
)

st.info(
    f"Expected ROP improvement: {improvement:.1f}%"
)

# ---------------------------------
# Feature Importance
# ---------------------------------

try:

    importance_df = pd.read_csv(
        "models/mwd/rop_feature_importance.csv"
    )

    st.subheader(
        "ROP Drivers"
    )

    chart_df = importance_df.copy()

    chart_df["feature"] = (
        chart_df["feature"]
        .str.replace("_", " ")
        .str.title()
    )

    chart_df = chart_df.set_index(
        "feature"
    )

    st.bar_chart(
        chart_df["importance"]
    )

except:
    pass
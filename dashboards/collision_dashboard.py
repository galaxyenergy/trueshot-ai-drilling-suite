import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.set_page_config(
    page_title="TrueShot AI Anti-Collision Monitor",
    layout="wide"
)

st.title("TrueShot AI Anti-Collision Monitor")

st.caption(
    "AI-Based Well Collision Prevention System"
)

model = joblib.load(
    "models/collision_rf.pkl"
)

st.subheader("Current Well Coordinates")

col1, col2, col3 = st.columns(3)

with col1:
    current_northing = st.number_input(
        "Current Northing",
        value=25000.0
    )

with col2:
    current_easting = st.number_input(
        "Current Easting",
        value=22000.0
    )

with col3:
    current_tvd = st.number_input(
        "Current TVD",
        value=20000.0
    )

st.subheader("Offset Well Coordinates")

col1, col2, col3 = st.columns(3)

with col1:
    offset_northing = st.number_input(
        "Offset Northing",
        value=26000.0
    )

with col2:
    offset_easting = st.number_input(
        "Offset Easting",
        value=22500.0
    )

with col3:
    offset_tvd = st.number_input(
        "Offset TVD",
        value=20100.0
    )

input_data = pd.DataFrame(
    [[
        current_northing,
        current_easting,
        current_tvd,
        offset_northing,
        offset_easting,
        offset_tvd
    ]],
    columns=[
        "current_northing",
        "current_easting",
        "current_tvd",
        "offset_northing",
        "offset_easting",
        "offset_tvd"
    ]
)

probability = model.predict_proba(input_data)[0][1]

distance = np.sqrt(
    (current_northing-offset_northing)**2
    +
    (current_easting-offset_easting)**2
    +
    (current_tvd-offset_tvd)**2
)

st.subheader("Collision Analysis")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Separation Distance",
        f"{distance:.1f} ft"
    )

with col2:
    st.metric(
        "Collision Probability",
        f"{probability*100:.1f}%"
    )

if probability < 0.30:

    st.success(
        "🟢 SAFE"
    )

    st.info(
        """
        Continue drilling.

        No immediate collision concerns detected.
        """
    )

elif probability < 0.70:

    st.warning(
        "🟡 MONITOR"
    )

    st.warning(
        """
        Review offset well trajectory.

        Increase survey frequency.

        Monitor separation factor.
        """
    )

else:

    st.error(
        "🔴 CRITICAL"
    )

    st.error(
        """
        Immediate anti-collision review required.

        Suspend drilling until cleared.
        """
    )

st.subheader("Well Position Map")

plot_df = pd.DataFrame({
    "Northing":[
        current_northing,
        offset_northing
    ],
    "Easting":[
        current_easting,
        offset_easting
    ]
})

st.scatter_chart(
    plot_df,
    x="Easting",
    y="Northing"
)
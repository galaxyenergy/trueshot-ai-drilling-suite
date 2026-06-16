import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Anti-Collision Monitoring",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ Anti-Collision Monitoring")

st.caption(
    "Real-time offset well proximity and collision risk monitoring"
)


depth = np.arange(0, 20001, 100)

distance = (
    60
    - 0.002 * depth
    + np.random.normal(0, 2, len(depth))
)

distance = np.clip(distance, 15, None)

df = pd.DataFrame({
    "depth": depth,
    "distance": distance
})


min_sep = df["distance"].min()
current_sep = df["distance"].iloc[-1]

high_risk_points = (df["distance"] < 25).sum()

risk_level = (
    "HIGH"
    if min_sep < 25
    else "MEDIUM"
    if min_sep < 50
    else "LOW"
)


closest_depth = df.loc[
    df["distance"].idxmin(),
    "depth"
]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Minimum Separation",
        f"{df['distance'].min():.1f} ft"
    )

with col2:
    st.metric(
        "Current Separation",
        f"{df['distance'].iloc[-1]:.1f} ft"
    )

with col3:
    st.metric(
        "High Risk Points",
        high_risk_points
    )

with col4:
    st.metric(
        "Closest Approach Depth",
        f"{closest_depth:,.0f} ft"
    )

with col5:
    st.metric(
        "Risk Level",
        risk_level
    )


st.subheader("Separation Distance vs Depth")

fig_sep = px.line(
    df,
    x="depth",
    y="distance",
    title="Offset Well Separation"
)

fig_sep.add_hline(
    y=30,
    line_dash="dash",
    line_color="red",
    annotation_text="Collision Threshold"
)


st.plotly_chart(
    fig_sep,
    width="stretch"
)

fig_sep.add_hline(
    y=30,
    line_dash="dash",
    line_color="red",
    annotation_text="Collision Threshold"
)



st.subheader("Collision Risk Assessment")
if min_sep > 50:
    st.success(
        "🟢 Low collision risk detected"
    )

elif min_sep > 25:
    st.warning(
        "🟡 Monitor offset well separation"
    )

else:
    st.error(
        "🔴 Collision risk exceeds company threshold"
    )
    
    
    offset_df = pd.DataFrame({
    "Offset Well":[
        "State 15-1H",
        "Johnson 12-3H",
        "Permian 22-7H"
    ],
    "Distance (ft)":[65,42,18],
    "Risk":["Low","Medium","High"]
})


st.subheader("AI Insights")
if min_sep < 25:

    st.error(
        "⚠️ Offset well proximity below safe threshold. Immediate review recommended."
    )

elif min_sep < 50:

    st.warning(
        "⚠️ Separation distance decreasing. Continue monitoring."
    )

else:

    st.success(
        "✅ Offset well separation remains within acceptable limits."
    )
    













def color_risk(val):
    if val == "Low":
        return "background-color: lightgreen"
    elif val == "Medium":
        return "background-color: khaki"
    elif val == "High":
        return "background-color: salmon"
    return ""

styled = offset_df.style.map(
    color_risk,
    subset=["Risk"]
)

st.dataframe(
    styled,
    use_container_width=True
)
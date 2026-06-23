import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="TrueShot AI - Torque & Drag",
    page_icon="🔩",
    layout="wide"
)

st.title("🔩 Torque & Drag Analytics")

st.caption(
    "Real-time torque, hookload and drag monitoring for drilling performance optimization"
)

# --------------------------------------------------
# SAMPLE DATA
# --------------------------------------------------

if "torque_df" not in st.session_state:
    st.warning("Please upload Torque CSV in Data Manager.")
    st.stop()

df = st.session_state["torque_df"]

#st.write(df.columns.tolist())

depth = np.arange(0, 20001, 100)

depth = df["Depth"]
hookload = df["Hookload"]
torque = df["Torque"]
#st.write(df.columns.tolist())

#hookload = df.iloc[:,1]
#torque = df.iloc[:,2]

drag = hookload * 0.08

df = pd.DataFrame({
    "depth": depth,
    "hookload": hookload,
    "torque": torque,
    "drag": drag
})

# --------------------------------------------------
# KPIs
# --------------------------------------------------

col1, col2, col3, col4, col5 = st.columns([2,2,2,2,1])

with col1:
    st.metric(
        "Current Hookload",
        f"{hookload.iloc[-1]:.1f} klbs"
    )

with col2:
    st.metric(
        "Current Torque",
        f"{torque.iloc[-1]:,.0f} ft-lbs"
    )

with col3:
    st.metric(
        "Max Torque",
        f"{torque.max():,.0f} ft-lbs"
    )

with col4:
    st.metric(
        "Drag Index",
        f"{drag.iloc[-1]:.1f}"
    )

with col5:
    st.metric(
        "Friction Factor",
        f"{np.mean(drag)/10:.2f}"
    )

# --------------------------------------------------
# HOOKLOAD
# --------------------------------------------------

st.subheader("Hookload vs Depth")

fig_hook = px.line(
    df,
    x="depth",
    y="hookload",
    title="Hookload Profile"
)

hookload_limit = 220

fig_hook.add_hline(
    y=hookload_limit,
    line_dash="dash",
    line_color="orange",
    annotation_text="Hookload Limit"
)

st.plotly_chart(
    fig_hook,
    use_container_width=True
)

# --------------------------------------------------
# TORQUE
# --------------------------------------------------

st.subheader("Torque vs Depth")

fig_torque = px.line(
    df,
    x="depth",
    y="torque",
    title="Torque Profile"
)

fig_torque.add_hline(
    y=4000,
    line_dash="dash",
    line_color="red",
    annotation_text="Torque Limit",
    annotation_position="top right"
)


st.plotly_chart(
    fig_torque,
    use_container_width=True
)

# --------------------------------------------------
# DRAG TREND
# --------------------------------------------------

df["drag_avg"] = df["drag"].rolling(10).mean()

st.subheader("Drag Trend")

fig_drag = px.line(
    df,
    x="depth",
    y="drag_avg",
    title="Rolling Average Drag"
)

drag_limit = 18

fig_drag.add_hline(
    y=drag_limit,
    line_dash="dash",
    line_color="orange",
    annotation_text="Drag Limit"
)

st.plotly_chart(
    fig_drag,
    width="stretch"
)

# --------------------------------------------------
# SECTION PERFORMANCE
# --------------------------------------------------

bins = [0, 5000, 10000, 15000, 20000]

labels = [
    "Surface",
    "Intermediate",
    "Curve",
    "Lateral"
]

df["zone"] = pd.cut(
    df["depth"],
    bins=bins,
    labels=labels
)

zone_table = (
    df.groupby("zone")["torque"]
      .mean()
      .reset_index()
)

zone_table.columns = [
    "Zone",
    "Average Torque (ft-lbs)"
]

zone_table["Average Torque (ft-lbs)"] = (
    zone_table["Average Torque (ft-lbs)"]
    .round(0)
    .astype(int)
)

if zone_table["Average Torque (ft-lbs)"].max() > 3500: 

 st.subheader("Formation Torque Analysis")

st.dataframe(
    zone_table,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------

st.subheader("AI Insights")

if torque.max() > 4500:
    st.error(
        "🚨 Torque exceeds recommended operating limit in lateral section."
    )

elif torque.max() > 4000:
    st.warning(
        "⚠️ Torque approaching operating limit. Monitor friction and hole cleaning."
    )

else:
    st.success(
        "✅ Torque remains within recommended operating range."
    )

# Separate insights
st.warning(
    "⚠️ Drag trend increasing with depth. Review hole cleaning and friction factors."
)

st.info(
    "ℹ️ Lateral section exhibits highest mechanical loading."
)

if drag.iloc[-1] > drag.mean() * 1.2:
    st.warning(
        "⚠️ Drag trend increasing. Review wellbore friction conditions."
    )

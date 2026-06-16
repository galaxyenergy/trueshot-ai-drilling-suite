import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="TrueShot AI - ROP Optimization",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ ROP Optimization")
st.caption("Rate of Penetration analytics and drilling performance monitoring")

depth = np.arange(0, 20000, 100)

rop = (
    120
    + 20*np.sin(depth/1500)
    + np.random.normal(0,5,len(depth))
)

df = pd.DataFrame({
    "depth": depth,
    "rop": rop
})

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Current ROP", f"{df['rop'].iloc[-1]:.1f} ft/hr")

with col2:
    st.metric("Average ROP", f"{df['rop'].mean():.1f} ft/hr")

with col3:
    st.metric("Best ROP", f"{df['rop'].max():.1f} ft/hr")

with col4:
    st.metric("Worst ROP", f"{df['rop'].min():.1f} ft/hr")
    
    
st.subheader("ROP vs Depth")

fig_rop = px.line(
    df,
    x="depth",
    y="rop",
    title="Rate of Penetration"
)

st.plotly_chart(
    fig_rop,
    width="stretch"
)

df["rop_avg"] = df["rop"].rolling(10).mean()

st.subheader("ROP Trend")

fig_avg = px.line(
    df,
    x="depth",
    y="rop_avg",
    title="Rolling Average ROP"
)

st.plotly_chart(
    fig_avg,
    width="stretch"
)

  
df["rop_avg"] = df["rop"].rolling(10).mean()


fig_avg = px.line(
    df,
    x="depth",
    y="rop_avg",
    title="Rolling Average ROP"
)

zone_labels = []

for md in depth:
    if md < 5000:
        zone_labels.append("Surface")
    elif md < 10000:
        zone_labels.append("Intermediate")
    elif md < 15000:
        zone_labels.append("Curve")
    else:
        zone_labels.append("Lateral")

df["Zone"] = zone_labels

zone_perf = (
    df.groupby("Zone")["rop"]
      .mean()
      .reset_index()
      .rename(columns={"rop":"Average ROP (ft/hr)"})
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



st.subheader("Formation Performance")
zone_perf["Average ROP (ft/hr)"] = (
    zone_perf["Average ROP (ft/hr)"]
    .round(1)
)

st.dataframe(
    zone_perf,
    hide_index=True,
    use_container_width=True
)



st.subheader("AI Insights")

if df["rop"].iloc[-1] < df["rop"].mean() * 0.8:
    st.warning(
        "⚠ ROP is significantly below average. Investigate bit wear or formation change."
    )
else:
    st.success(
        "✅ ROP is operating within expected range."
    )   
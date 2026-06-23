import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("🌊 Hydraulics Optimization")

st.caption(
    "Real-time hydraulics monitoring for drilling efficiency and hole cleaning"
)

if "hydraulics_df" not in st.session_state:
    st.warning("Please upload Hydraulics CSV in Data Manager.")
    st.stop()

df = st.session_state["hydraulics_df"]

#st.write(df.columns.tolist())
#st.stop()

#depth = np.arange(0, 20001, 100)

depth = df["Depth"]
flowrate = df["FlowRate"]
spp = df["SPP"]
ecd = df["ECD"]
mudweight = df["MudWeight"]
annular_velocity = df["AnnularVelocity"]

hp = (spp * flowrate) / 1714

col1,col2,col3,col4,col5 = st.columns(5)

col1.metric(
    "Current ECD_ppg",
    f"{ecd.iloc[-1]:.2f} ppg"
)

col2.metric(
    "Current SPP_psi",
    f"{spp.iloc[-1]:.0f} psi"
)

col3.metric(
    "Hydraulic_HP",
    f"{hp.iloc[-1]:.0f}"
)

col4.metric(
    "Max ECD_ppg",
    f"{ecd.max():.2f}"
)

col5.metric(
    "Hole Cleaning",
    "92%"
)

depth = np.arange(0, 20001, 100)

ecd = (
    10
    + (depth / 20000) * 1.6
    + np.random.normal(0, 0.08, len(depth))
)

spp = (
    1800
    + (depth / 20000) * 2400
    + np.random.normal(0, 40, len(depth))
)

hp = (
    350
    + (depth / 20000) * 210
    + np.random.normal(0, 10, len(depth))
)

df = pd.DataFrame({
    "depth": depth,
    "ecd": ecd,
    "spp": spp,
    "hp": hp
})

fig_ecd = px.line(
    df,
    x="depth",
    y="ecd",
    title="Equivalent Circulating Density",
    labels={
        "depth": "Measured Depth (ft)",
        "ecd": "ECD (ppg)"
    }
)

fig_ecd.add_hline(
    y=11.5,
    line_dash="dash",
    line_color="red",
    annotation_text="Fracture Limit"
)

st.plotly_chart(
    fig_ecd,
    width="stretch"
)

fig_spp = px.line(
    df,
    x="depth",
    y="spp",
    title="Standpipe Pressure",
    labels={
        "depth": "Measured Depth (ft)",
        "spp": "Standpipe Pressure (psi)"
    }
)

fig_spp.add_hline(
    y=4000,
    line_dash="dash",
    line_color="orange",
    annotation_text="SPP_psi Limit"
)

st.plotly_chart(
    fig_spp,
    width="stretch"
)

fig_hp = px.line(
    df,
    x="depth",
    y="hp",
    title="Hydraulic Horsepower",
    labels={
        "depth": "Measured Depth (ft)",
        "hp": "Hydraulic Horsepower"
    }
)

st.plotly_chart(
    fig_hp,
    width="stretch"
)

bins = [0,5000,10000,15000,20000]

labels = [
    "Surface",
    "Intermediate",
    "Curve",
    "Lateral"
]

df = pd.DataFrame({
    "depth": depth,
    "ecd": ecd
})

df["zone"] = pd.cut(
    df["depth"],
    bins=bins,
    labels=labels
)

zone_table = (
    df.groupby("zone")["ecd"]
    .mean()
    .reset_index()
)

zone_table.columns = [
    "Zone",
    "Average ECD_ppg"
]

st.subheader(
    "Formation Hydraulics Analysis"
)

st.dataframe(
    zone_table,
    hide_index=True
)

st.subheader("AI Insights")

hole_cleaning = 92

if hole_cleaning > 90:
    st.success("Hole cleaning efficiency remains acceptable.")
else:
    st.warning("Hole cleaning efficiency deteriorating.")
   
if ecd.max() > 11.5:
    st.error(
        "🚨 ECD approaching fracture gradient in lateral section."
    )
    
if spp[-1] > spp.mean()*1.2:
    st.warning(
        "⚠️ Standpipe pressure increasing with depth."
    )
    
st.info(
    "ℹ️ Hydraulic horsepower remains within target operating range."
)

        


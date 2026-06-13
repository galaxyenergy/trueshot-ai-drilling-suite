import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="TrueShot DD Dashboard",
    layout="wide"
)

st.title("TrueShot AI Directional Drilling Dashboard")

df = pd.read_csv(
    "data/dd_timeseries_v1.csv"
)

current = df.iloc[-1]

# ---------------------------
# Top Metrics
# ---------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Current MD",
        f"{current['md']:.0f} ft"
    )

with col2:
    st.metric(
        "Current TVD",
        f"{current['tvd']:.0f} ft"
    )

with col3:
    st.metric(
        "Current Inclination",
        f"{current['inc']:.1f}°"
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Current Azimuth",
        f"{current['azi']:.1f}°"
    )

with col5:
    st.metric(
        "Current DLS",
        f"{current['dls']:.1f}"
    )

with col6:
    st.metric(
        "Current ROP",
        f"{current['rop']:.0f} ft/hr"
    )

# ---------------------------
# Performance Summary
# ---------------------------

st.subheader("Drilling Performance")

col7, col8, col9 = st.columns(3)

with col7:
    st.metric(
        "Average Slide %",
        f"{df['slide_pct'].mean():.1f}%"
    )

with col8:
    st.metric(
        "Average RPM",
        f"{df['rpm'].mean():.0f}"
    )

with col9:
    st.metric(
        "Average WOB",
        f"{df['wob'].mean():.0f}"
    )

# ---------------------------
# Charts
# ---------------------------

st.subheader("Inclination Trend")

st.line_chart(
    df.set_index("md")["inc"]
)

st.subheader("Azimuth Trend")

st.line_chart(
    df.set_index("md")["azi"]
)

st.subheader("Dogleg Severity")

st.line_chart(
    df.set_index("md")["dls"]
)

st.subheader("Vertical Section")

st.line_chart(
    df.set_index("md")["vertical_section"]
)

st.subheader("Well Path")

wellpath = (
    df[["northing", "easting"]]
    .tail(3000)
)

st.line_chart(wellpath)
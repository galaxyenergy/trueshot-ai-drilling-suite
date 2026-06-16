import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="TrueShot AI - Directional Drilling",
    page_icon="🧭",
    layout="wide"
)

st.title("🧭 Directional Drilling Analytics")

st.caption(
    "Wellbore trajectory monitoring and directional performance analytics"
)

df = pd.read_csv("data/mwd/Sample_MWD_Survey.csv")

#st.write(df.head())
#st.write(df.columns)

depth = df["MD_ft"].values
inclination = df["INC_deg"].values
azimuth = df["AZI_deg"].values

st.metric(
    "Total Depth",
    f"{depth[-1]:,.0f} ft"
)

st.metric(
    "Final Inclination",
    f"{inclination[-1]:.2f}°"
)

st.metric(
    "Final Azimuth",
    f"{azimuth[-1]:.2f}°"
)

dogleg = [0]

for i in range(1, len(depth)):
    dmd = depth[i] - depth[i-1]

    dinc = inclination[i] - inclination[i-1]
    dazi = azimuth[i] - azimuth[i-1]

    dls = np.sqrt(dinc**2 + dazi**2) * 100 / dmd

    dogleg.append(dls)

dogleg = np.array(dogleg)

# Calculate TVD, Northing, Easting

tvd = [0]
northing = [0]
easting = [0]

for i in range(1, len(depth)):

    dmd = depth[i] - depth[i-1]

    inc_avg = np.radians(
        (inclination[i] + inclination[i-1]) / 2
    )

    azi_avg = np.radians(
        (azimuth[i] + azimuth[i-1]) / 2
    )

    dtvd = dmd * np.cos(inc_avg)

    dnorth = dmd * np.sin(inc_avg) * np.cos(azi_avg)

    deast = dmd * np.sin(inc_avg) * np.sin(azi_avg)

    tvd.append(tvd[-1] + dtvd)
    northing.append(northing[-1] + dnorth)
    easting.append(easting[-1] + deast)

tvd = np.array(tvd)
northing = np.array(northing)
easting = np.array(easting)


df = pd.DataFrame({
    "depth": depth,
    "inclination": inclination,
    "azimuth": azimuth,
    "dogleg": dogleg,
    "tvd": tvd,
    "northing": northing,
    "easting": easting
})


st.subheader("Inclination Profile")

fig_inc = px.line(
    df,
    x="depth",
    y="inclination",
    title="Inclination vs Measured Depth"
)

st.plotly_chart(fig_inc, width="stretch")


st.subheader("Azimuth Profile")

fig_azi = px.line(
    df,
    x="depth",
    y="azimuth",
    title="Azimuth vs Measured Depth"
)

st.plotly_chart(fig_azi, width="stretch")

st.subheader("Vertical Section")

fig_vs = px.line(
    df,
    x="easting",
    y="tvd",
    title="Vertical Section"
)

fig_vs.update_yaxes(
    autorange="reversed"
)

st.plotly_chart(
    fig_vs,
    width="stretch"
)


import plotly.graph_objects as go

st.subheader("3D Wellbore")

fig_3d = go.Figure()

fig_3d.add_trace(
    go.Scatter3d(
        x=df["easting"],
        y=df["northing"],
        z=-df["tvd"],
        mode="lines",
        line=dict(width=6)
    )
)

fig_3d.update_layout(
    scene=dict(
        xaxis_title="Easting",
        yaxis_title="Northing",
        zaxis_title="TVD"
    ),
    height=700
)

st.plotly_chart(
    fig_3d,
    width="stretch"
)

st.subheader("Plan View")

fig_plan = px.line(
    df,
    x="easting",
    y="northing",
    title="Well Path Plan View"
)

st.plotly_chart(
    fig_plan,
    use_container_width=True
)


#st.write(df.tail())
#st.stop()


if dogleg.max() < 4:
    st.success("🟢 Well path within directional limits")

elif dogleg.max() < 6:
    st.warning("🟡 Monitor dogleg severity")

else:
    st.error("🔴 High dogleg severity detected")
    

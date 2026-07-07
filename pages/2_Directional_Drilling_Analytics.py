import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.auth_guard import require_login
from utils.datasource import get_module_data
from services.shift_analysis_service import build_current_shift_analysis
from services.survey_export_service import generate_survey_files_from_templates



st.set_page_config(
    page_title="TrueShot AI - Directional Drilling",
    page_icon="🧭",
    layout="wide"
)

require_login()


st.title("🧭 Directional Drilling Analytics")

st.caption(
    "Wellbore trajectory monitoring and directional performance analytics"
)

df = get_module_data("directional_df")

if df is None or df.empty:
    st.warning("Please import a WellData export in Operations Data Center.")
    st.stop()

st.session_state["directional_df"] = df
st.session_state["survey_df"] = df


#st.write(df.columns.tolist())
#st.stop()

depth = df["MD"].values
inclination = df["Inc"].values
azimuth = df["Azm"].values

tvd = df["TVD"].values
northing = df["Northing"].values
easting = df["Easting"].values
dogleg = df["Dogleg"].values

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

    dls = 0 if dmd == 0 or pd.isna(dmd) else np.sqrt((dinc**2 + dazi**2)) * 100 / dmd

    dogleg.append(dls)

dogleg = df["Dogleg"].values

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

st.plotly_chart(fig_inc, width="stretch"
)

#st.write(df.tail())
#st.stop()

if dogleg.max() < 4:
    st.success("🟢 Well path within directional limits")

elif dogleg.max() < 6:
    st.warning("🟡 Monitor dogleg severity")

else:
    st.error("🔴 High dogleg severity detected")
    


# ==================================================
# SURVEY EXPORT CENTER
# ==================================================

st.divider()

st.subheader("Survey Export Center")

st.write(
    "Generate TrueShot and Oxy survey files from the uploaded TrueShot survey template."
)

if st.button("Generate TrueShot and Oxy Survey Files"):
    try:
        survey_result = generate_survey_files_from_templates()

        survey_df = survey_result["survey_df"]
        trueshot_file = survey_result["trueshot_file"]
        oxy_file = survey_result["oxy_file"]

        st.session_state["generated_survey_df"] = survey_df
        st.session_state["generated_trueshot_file"] = trueshot_file
        st.session_state["generated_oxy_file"] = oxy_file

        st.success("Survey files generated successfully.")

    except Exception as e:
        st.error(f"Survey generation failed: {e}")


if "generated_survey_df" in st.session_state:
    st.subheader("Survey Data Preview")

if "generated_survey_df" in st.session_state:
    st.subheader("Survey Data Preview")

    st.dataframe(
        st.session_state["generated_survey_df"],
        width="stretch",
        hide_index=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="Download TRUEshot Survey File",
            data=st.session_state["generated_trueshot_file"],
            file_name="generated_trueshot_survey.xlsm",
            mime="application/vnd.ms-excel.sheet.macroEnabled.12"
        )

    with col2:
        st.download_button(
            label="Download Oxy Survey File",
            data=st.session_state["generated_oxy_file"],
            file_name="generated_oxy_survey.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )        
       
    

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="Download TrueShot Survey File",
            data=st.session_state["generated_trueshot_file"],
            file_name="generated_trueshot_survey.xlsm",
            mime="application/vnd.ms-excel.sheet.macroEnabled.12"
        )

    with col2:
        st.download_button(
            label="Download Oxy Survey File",
            data=st.session_state["generated_oxy_file"],
            file_name="generated_oxy_survey.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
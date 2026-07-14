import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.auth_guard import require_login
from utils.datasource import get_module_data
from services.shift_analysis_service import build_current_shift_analysis
from services.survey_export_service import generate_survey_files_from_templates
from services.survey_export_service import (
    generate_survey_files_from_uploaded_data,
    read_corrected_survey_upload,
)


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

st.plotly_chart(
    fig_inc,
    width="stretch",
    key="directional_inclination_chart"
)

st.subheader("Azimuth Profile")

fig_azi = px.line(
    df,
    x="depth",
    y="azimuth",
    title="Azimuth vs Measured Depth"
)

st.plotly_chart(
    fig_azi,
    width="stretch",
    key="directional_azimuth_chart"
)

st.subheader("Vertical Section")

fig_vs = px.line(
    df,
    x="easting",
    y="tvd",
    title="Vertical Section"
)

st.plotly_chart(
    fig_vs,
    width="stretch",
    key="directional_tvd_chart"
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

# ==================================================
# CORRECTED SURVEY FILE UPLOAD
# ==================================================

st.subheader("Upload Corrected Survey File")

corrected_survey_file = st.file_uploader(
    "Upload corrected survey file for accurate directional reporting",
    type=["csv", "xlsx", "xlsm"],
    key="corrected_survey_file_upload"
)

if corrected_survey_file is not None:
    try:
        corrected_survey_df = read_corrected_survey_upload(corrected_survey_file)

        st.session_state["survey_df"] = corrected_survey_df
        st.session_state["directional_df"] = corrected_survey_df
        st.session_state["corrected_survey_df"] = corrected_survey_df

        st.success("Corrected survey file loaded successfully.")

        st.dataframe(
            corrected_survey_df.head(50),
            width="stretch",
            hide_index=True
        )

    except Exception as e:
        st.error(f"Corrected survey upload failed: {e}")
        


# ==================================================
# SURVEY DATA STATUS
# ==================================================

st.subheader("Survey Data Status")

corrected_survey_df = st.session_state.get("corrected_survey_df")
survey_df = st.session_state.get("survey_df")
directional_df = st.session_state.get("directional_df")
standard_df = st.session_state.get("standard_df")

survey_source = "None"
survey_status = "MISSING"
survey_rows = 0
survey_message = "No valid survey data is available yet."

if corrected_survey_df is not None and not corrected_survey_df.empty:
    survey_source = "Corrected Survey Upload"
    survey_status = "PASS"
    survey_rows = len(corrected_survey_df)
    survey_message = "Corrected survey file is loaded and will be used for TRUEshot/Oxy survey generation."

elif survey_df is not None and not survey_df.empty:
    survey_source = "Extracted Survey Data"
    survey_status = "PASS"
    survey_rows = len(survey_df)
    survey_message = "Survey data was extracted from the uploaded Operations Data Center file."

elif directional_df is not None and not directional_df.empty:
    survey_source = "Directional Data"
    survey_status = "PASS"
    survey_rows = len(directional_df)
    survey_message = "Directional data is available."

elif standard_df is not None and not standard_df.empty:
    survey_source = "Operations Data Center"
    survey_status = "SURVEY MISSING"
    survey_rows = 0
    survey_message = "Operations data is available, but no valid MD / Inclination / Azimuth survey data was found."

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Survey Status", survey_status)

with col2:
    st.metric("Survey Source", survey_source)

with col3:
    st.metric("Survey Rows", f"{survey_rows:,}")

if survey_status == "PASS":
    st.success(survey_message)
else:
    st.warning(
        survey_message
        + " Upload a corrected survey file before generating TrueShot or Oxy survey reports."
    )



st.write(
    "Generate TrueShot and Oxy survey files from the uploaded TrueShot survey template."
)

if st.button("Generate TrueShot and Oxy Survey Files"):
    try:
        source_df = st.session_state.get("corrected_survey_df")

        if source_df is None or source_df.empty:
            source_df = st.session_state.get("survey_df")

        if source_df is None or source_df.empty:
            source_df = st.session_state.get("standard_df")

        survey_result = generate_survey_files_from_uploaded_data(source_df)

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

    preview_df = st.session_state["generated_survey_df"].copy()

    # Clean mixed data types before displaying in Streamlit
    for col in preview_df.columns:
        preview_df[col] = preview_df[col].apply(
            lambda x: x.decode("utf-8", errors="ignore") if isinstance(x, bytes) else x
        )

        if preview_df[col].dtype == "object":
            preview_df[col] = preview_df[col].astype(str)

    st.dataframe(
        preview_df,
        width="stretch",
        hide_index=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="Download TrueShot Survey File",
            data=st.session_state["generated_trueshot_file"],
            file_name="generated_trueshot_survey.xlsm",
            mime="application/vnd.ms-excel.sheet.macroEnabled.12",
            key="download_generated_trueshot_survey"
        )

    with col2:
        st.download_button(
            label="Download Oxy Survey File",
            data=st.session_state["generated_oxy_file"],
            file_name="generated_oxy_survey.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_generated_oxy_survey"
        )
        
        
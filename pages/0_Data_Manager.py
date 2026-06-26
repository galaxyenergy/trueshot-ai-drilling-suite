import streamlit as st
import pandas as pd
import numpy as np

def clean_dataset(df):

    original_rows = len(df)

    # Remove duplicates
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()

    # Missing values
    missing_before = df.isnull().sum().sum()

    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        df[col] = df[col].interpolate()
        df[col] = df[col].fillna(df[col].median())

    missing_after = df.isnull().sum().sum()

    return {
        "df": df,
        "rows": original_rows,
        "duplicates": duplicates,
        "missing_before": missing_before,
        "missing_after": missing_after
    }

st.set_page_config(
    page_title="Data Manager",
    page_icon="📂",
    layout="wide"
)

st.title("📂 Data Manager")
st.caption("Upload well data files for all analytics modules")

# --------------------------------------------------
# SURVEY DATA
# --------------------------------------------------
survey_file = st.file_uploader(
    "Upload Directional Survey",
    type=["csv"],
    key="survey"
)

if survey_file:

    raw_df = pd.read_csv(survey_file)

    result = clean_dataset(raw_df)

    st.session_state["survey_df"] = result["df"]

    st.success(
        f"Survey loaded: {len(result['df'])} rows"
    )

    st.write("Duplicates Removed:", result["duplicates"])
    st.write("Missing Values Before:", result["missing_before"])
    st.write("Missing Values After:", result["missing_after"])

# --------------------------------------------------
# MWD DATA
# --------------------------------------------------

mwd_file = st.file_uploader(
    "Upload MWD Data",
    type=["csv"],
    key="mwd"
)

if mwd_file:

    raw_df = pd.read_csv(mwd_file)

    result = clean_dataset(raw_df)

    st.session_state["mwd_df"] = result["df"]

    st.success(
        f"MWD loaded: {len(result['df'])} rows"
    )

    st.write("Duplicates Removed:", result["duplicates"])
    st.write("Missing Values Before:", result["missing_before"])
    st.write("Missing Values After:", result["missing_after"])

# --------------------------------------------------
# ROP DATA
# --------------------------------------------------

rop_file = st.file_uploader(
    "Upload Drilling Performance Data",
    type=["csv"],
    key="rop"
)

if rop_file:

    raw_df = pd.read_csv(rop_file)

    result = clean_dataset(raw_df)

    st.session_state["rop_df"] = result["df"]

    st.success(
        f"ROP loaded: {len(result['df'])} rows"
    )

    st.write("Duplicates Removed:", result["duplicates"])
    st.write("Missing Values Before:", result["missing_before"])
    st.write("Missing Values After:", result["missing_after"])
    
 # --------------------------------------------------
# COLLISION DATA
# --------------------------------------------------

collision_file = st.file_uploader(
    "Upload Anti-Collision Data",
    type=["csv"],
    key="collision"
)

if collision_file:

    raw_df = pd.read_csv(collision_file)

    result = clean_dataset(raw_df)

    st.session_state["collision_df"] = result["df"]

    st.success(
        f"Collision loaded: {len(result['df'])} rows"
    )

    st.write("Duplicates Removed:", result["duplicates"])
    st.write("Missing Values Before:", result["missing_before"])
    st.write("Missing Values After:", result["missing_after"])

# --------------------------------------------------
# TORQUE / DRAG DATA
# --------------------------------------------------

torque_file = st.file_uploader(
    "Upload Torque & Drag Data",
    type=["csv"],
    key="torque"
)

if torque_file:

    raw_df = pd.read_csv(torque_file)

    result = clean_dataset(raw_df)

    st.session_state["torque_df"] = result["df"]

    st.success(
        f"Torque loaded: {len(result['df'])} rows"
    )

    st.write("Duplicates Removed:", result["duplicates"])
    st.write("Missing Values Before:", result["missing_before"])
    st.write("Missing Values After:", result["missing_after"])

# --------------------------------------------------
# HYDRAULICS DATA
# --------------------------------------------------

hyd_file = st.file_uploader(
    "Upload Hydraulics Data",
    type=["csv"],
    key="hydraulics"
)

if hyd_file:

    raw_df = pd.read_csv(hyd_file)

    result = clean_dataset(raw_df)

    st.session_state["hydraulics_df"] = result["df"]

    st.success(
        f"Hydraulics loaded: {len(result['df'])} rows"
    )

    st.write("Duplicates Removed:", result["duplicates"])
    st.write("Missing Values Before:", result["missing_before"])
    st.write("Missing Values After:", result["missing_after"])

# --------------------------------------------------
# STATUS PANEL
# --------------------------------------------------

st.divider()

st.subheader("Loaded Datasets")

st.write(
    {
        "Survey": "✅" if "survey_df" in st.session_state else "❌",
        "MWD": "✅" if "mwd_df" in st.session_state else "❌",
        "ROP": "✅" if "rop_df" in st.session_state else "❌",
        "Collision": "✅" if "collision_df" in st.session_state else "❌",
        "Torque": "✅" if "torque_df" in st.session_state else "❌",
        "Hydraulics": "✅" if "hydraulics_df" in st.session_state else "❌",
    }
)



st.subheader("📊 Data Quality Dashboard")

if "survey_df" in st.session_state:
    st.success("Survey found")
else:
    st.error("Survey NOT found")



if "survey_df" in st.session_state:

    survey_df = st.session_state["survey_df"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Rows",
            len(survey_df)
        )

    with col2:
        st.metric(
            "Columns",
            len(survey_df.columns)
        )

    with col3:
        st.metric(
            "Missing Values",
            survey_df.isnull().sum().sum()
        )

    with col4:
        st.metric(
            "Duplicates",
            survey_df.duplicated().sum()
        )

    st.write("### Column Summary")

    st.dataframe(
        pd.DataFrame({
            "Column": survey_df.columns,
            "Data Type": survey_df.dtypes.astype(str)
        }),
        use_container_width=True
    )
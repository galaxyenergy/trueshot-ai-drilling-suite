import streamlit as st
import pandas as pd
from core.session_manager import SessionManager
from services.import_service import ImportService
from core.approved_dataset import ApprovedDataset
from utils.datasource import normalize_welldata_export
from utils.auth_guard import require_login
from services.edr_data_quality_service import clean_edr_dataframe

from services.mwd_directional_extractor import (
    extract_mwd_data,
    extract_directional_survey_data,
)

st.set_page_config(
    page_title="Operations Data Center",
    page_icon="🌐",
    layout="wide"
)
require_login()


context = SessionManager.get_context()

st.title("🌐 TrueShot Operations Data Center")
st.caption("Enterprise Data Integration & Well Management")

st.divider()

# =====================================================
# ORGANIZATION
# =====================================================

st.subheader("🏢 Organization")

col1, col2, col3, col4 = st.columns(4)

with col1:
    operator = st.selectbox(
        "Operator",
        [
            "Select Operator",
            "Chevron",
            "ExxonMobil",
            "Oxy",
            "ConocoPhillips",
            "Diamondback",
            "Conoco",
            "Ineos",
            "Cotera",
            "POP",
            "Pinnergy",
            "Diamondback",
            "Devon",
            "Double Eagle",
            "Shell",
            "EOG",
            "Apache",
            "Other"
        ]
    )

with col2:
    rig = st.selectbox(
        "Rig",
        [
            "Select Rig",
            "HP 537",
            "Primo 5",
            "Primo 7",
            "Primo 9",
            "Lasso 102",
            "Pinnergy 1",
            "Pinnergy 6",
            "Pinnergy 10",
            "Cactus 161",
            "X-23",
        ]
    )

with col3:
    well = st.selectbox(
        "Well",
        [
            "Select Well",
            "Schwope LAS B 2H",
            "Other",
        ]
    )

with col4:
    shift = st.radio(
        "Shift",
        [
            "Day Shift",
            "Night Shift"
        ]
    )

st.divider()

# =====================================================
# CONNECTION
# =====================================================

st.subheader("🔗 Connection Method")

connection = st.radio(
    "Connection Method",
    [
        "Periodic Data Synchronization",
        "Live Data Connection (Future)"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

if connection == "Periodic Data Synchronization":

    st.success(
        "Production Mode\n\n"
        "Import a full well export once per shift."
    )

else:

    st.info(
        "Future Capability\n\n"
        "Reserved for WITS / WITSML / Vendor API integrations."
    )

st.divider()

# =====================================================
# DATA SOURCE
# =====================================================

st.subheader("📂 Data Source")

source = st.selectbox(
    "Select Source",
    [
        "Pason WellData Export",
        "CSV",
        "Excel",
        "ASCII",
        "LAS",
        "WITSML",
        
    ]
)

st.divider()

# =====================================================
# IMPORT
# =====================================================

st.subheader("📥 Import")

left, right = st.columns(2)

with left:

    uploaded = st.file_uploader(
    "Browse Export",
    type=[
        "csv",
        "xlsx",
        "xls",
        "txt",
        "las",
        "xml"
    ],
    key="uploaded_file"
)

with right:

    st.write("")

import_btn = st.button(
    "Import Well Export",
    use_container_width=True
)

if import_btn:

    if uploaded is None:

        st.warning("Please select a WellData export.")

    else:

        with st.spinner("Importing shift export..."):

            dataset = ImportService.import_file(uploaded)
            
            clean_df, cleaning_summary, cleaning_report = clean_edr_dataframe(
                dataset.raw_dataframe
            )

            dataset.raw_dataframe = clean_df

            st.session_state["edr_cleaning_summary"] = cleaning_summary
            st.session_state["edr_cleaning_report"] = cleaning_report
            
            st.session_state["current_dataset"] = dataset
            
            # Save project metadata for reports
            dataset.operator = operator
            dataset.rig = rig
            dataset.well = well
            dataset.shift = shift

            st.session_state["operator_name"] = operator
            st.session_state["rig_name"] = rig
            st.session_state["well_name"] = well
            st.session_state["shift_name"] = shift
            st.session_state["shift_hours"] = 12
            
           
            # Temporary demo bridge: feed existing modules from Operations Data Center
            standard_df = normalize_welldata_export(dataset.raw_dataframe)
            
            mwd_only_df, mwd_extract_summary = extract_mwd_data(dataset.raw_dataframe)
            survey_only_df, survey_extract_summary = extract_directional_survey_data(dataset.raw_dataframe)

            st.session_state["mwd_only_df"] = mwd_only_df
            st.session_state["mwd_extract_summary"] = mwd_extract_summary

            st.session_state["survey_only_df"] = survey_only_df
            st.session_state["survey_extract_summary"] = survey_extract_summary
                                                  
            st.session_state["standard_df"] = standard_df

            # Existing module keys
            st.session_state["mwd_df"] = standard_df
            st.session_state["survey_df"] = standard_df
            
            st.session_state["mwd_df"] = mwd_only_df if not mwd_only_df.empty else standard_df

            if not survey_only_df.empty:
                st.session_state["survey_df"] = survey_only_df
                st.session_state["directional_df"] = survey_only_df
            else:
                st.session_state["survey_df"] = pd.DataFrame()
                st.session_state["directional_df"] = pd.DataFrame()
                                        
            st.session_state["rop_df"] = standard_df
            st.session_state["hydraulics_df"] = standard_df
            st.session_state["torque_df"] = standard_df

            # Extra safety keys for old pages
            st.session_state["directional_df"] = standard_df
            st.session_state["anti_collision_df"] = standard_df
            st.session_state["collision_df"] = standard_df
            st.session_state["report_df"] = standard_df
                        
                            
        st.success("Shift export imported successfully.")


analyze_btn = st.button(
    "Analyze Imported Data",
    use_container_width=True
)

# ======================================================
# ANALYZE IMPORTED DATA
# ======================================================

if analyze_btn:
    
    #st.error("ENTERED ANALYZE BUTTON")
    
    if "current_dataset" not in st.session_state:

        st.warning("Please import a WellData export first.")

    else:

        dataset: ApprovedDataset = st.session_state["current_dataset"]
        
        #st.success("DATASET LOADED")

        report = dataset.validation_report

        #st.success("REPORT LOADED")

st.subheader("MWD and Directional Data Extraction Summary")

mwd_summary = st.session_state.get("mwd_extract_summary", {})
survey_summary = st.session_state.get("survey_extract_summary", {})

c1, c2 = st.columns(2)

with c1:
    st.markdown("### MWD Channels")
    st.write(f"Status: {mwd_summary.get('status', 'UNKNOWN')}")
    st.write(f"Rows: {mwd_summary.get('rows', 0):,}")
    st.write(f"Columns: {mwd_summary.get('columns', 0):,}")

    found_channels = mwd_summary.get("found_channels", {})

    if found_channels:
        st.dataframe(
            pd.DataFrame(
                [{"Standard Channel": k, "Source Column": v} for k, v in found_channels.items()]
            ),
            width="stretch",
            hide_index=True
        )

with c2:
    st.markdown("### Directional / Survey Data")
    st.write(f"Status: {survey_summary.get('status', 'UNKNOWN')}")
    st.write(survey_summary.get("message", ""))

    source_columns = survey_summary.get("source_columns", {})

    if source_columns:
        st.dataframe(
            pd.DataFrame(
                [{"Survey Field": k, "Source Column": v} for k, v in source_columns.items()]
            ),
            width="stretch",
            hide_index=True
        )

    if survey_summary.get("status") != "PASS":
        st.warning(
            survey_summary.get(
                "recommendation",
                "Upload a corrected survey file for accurate directional reporting."
            )
        )



# ==================================================
# SHIFT EXECUTIVE DASHBOARD
# ==================================================             

        st.divider()

         
        st.subheader("📋 Import Summary")

        #st.success("ABOUT TO DISPLAY SUMMARY")
        
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**File Name:** {dataset.file_name}")
            st.write(f"**Rows:** {len(dataset.raw_dataframe):,}")

        with col2:
            st.write(f"**Columns:** {len(dataset.raw_dataframe.columns)}")
            st.write(f"**Imported:** {dataset.import_time.strftime('%Y-%m-%d %H:%M:%S')}")

        st.divider()


        st.subheader("📊 EDR Data Cleaning Summary")

        summary = st.session_state.get("edr_cleaning_summary", {})

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Status", summary.get("status", "UNKNOWN"))

        with c2:
            st.metric("Rows", f"{summary.get('cleaned_rows', 0):,}")

        with c3:
            st.metric(
                "Bad EDR Values Removed",
                f"{summary.get('total_bad_edr_values_removed', 0):,}"
            )

        with c4:
            st.metric(
                "Bad Columns Removed",
                summary.get("unnamed_columns_removed", 0)
                + summary.get("empty_columns_removed", 0)
            )

        cleaning_report = st.session_state.get("edr_cleaning_report")

        if cleaning_report is not None:
            st.subheader("Channel Cleaning Report")

            st.dataframe(
                cleaning_report,
                width="stretch",
                hide_index=True
            )


        st.divider()

        st.subheader("🔍 Cleaned Data Preview")

        standard_df = st.session_state.get("standard_df")

        if standard_df is not None:
            st.dataframe(
                standard_df.head(50),
                width="stretch"
            )

        st.divider()


        st.subheader("📋 Available Cleaned WellData Channels")

        standard_df = st.session_state.get("standard_df")

        if standard_df is not None:
            channels_df = pd.DataFrame(
                {
                    "No": range(1, len(standard_df.columns) + 1),
                    "Channel": list(standard_df.columns)
                }
            )

            st.dataframe(
                channels_df,
                width="stretch",
                hide_index=True
            )

# =====================================================
# HISTORY
# =====================================================

st.subheader("📜 Import History")

st.info(
    "Import history will appear here."
)

st.divider()

# =====================================================
# FUTURE MODULES
# =====================================================

st.subheader("🚀 Enterprise Roadmap")

col1, col2, col3 = st.columns(3)

with col1:

    st.success("✓ Multi Operator")

    st.success("✓ Multi Rig")

    st.success("✓ Multi Well")

    st.success("✓ Shift Management")

with col2:

    st.info("Survey Management")

    st.info("Survey Sheet Generator")

    st.info("Survey Downloads")

with col3:

    st.info("MWD Tool Management")

    st.info("Tool Dump Generator")

    st.info("Tool History")
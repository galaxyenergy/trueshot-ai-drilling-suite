import streamlit as st
import pandas as pd
from core.session_manager import SessionManager
from services.import_service import ImportService
from core.approved_dataset import ApprovedDataset




st.set_page_config(
    page_title="Operations Data Center",
    page_icon="🌐",
    layout="wide"
)

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

            st.session_state["current_dataset"] = dataset

        st.success("Shift export imported successfully.")



analyze_btn = st.button(
    "Analyze Imported Data",
    use_container_width=True
)

    # ======================================================
# ANALYZE IMPORTED DATA
# ======================================================

if analyze_btn:

    if "current_dataset" not in st.session_state:

        st.warning("Please import a WellData export first.")

    else:

        dataset: ApprovedDataset = st.session_state["current_dataset"]

        report = dataset.validation_report



        st.divider()

         

        st.subheader("📋 Import Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**File Name:** {dataset.file_name}")
            st.write(f"**Rows:** {len(dataset.raw_dataframe):,}")

        with col2:
            st.write(f"**Columns:** {len(dataset.raw_dataframe.columns)}")
            st.write(f"**Imported:** {dataset.import_time.strftime('%Y-%m-%d %H:%M:%S')}")

        st.divider()

        st.subheader("📊 Validation Summary")

        st.json(report)

        st.divider()

        st.subheader("🔍 Data Preview")

        st.dataframe(
            dataset.raw_dataframe.head(20),
            use_container_width=True
        )




st.divider()

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
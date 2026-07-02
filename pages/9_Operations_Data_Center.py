import streamlit as st

from core.session_manager import SessionManager


st.set_page_config(
    page_title="Operations Data Center",
    page_icon="🌐",
    layout="wide"
)

context = SessionManager.get_context()

st.title("🌐 Operations Data Center")
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
            "Other"
        ]
    )

with col2:
    rig = st.selectbox(
        "Rig",
        [
            "Select Rig"
        ]
    )

with col3:
    well = st.selectbox(
        "Well",
        [
            "Select Well"
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
        "WITSML"
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
            "txt",
            "las",
            "xml"
        ]
    )

with right:

    st.write("")

    st.write("")

    import_btn = st.button(
        "Import Well Export",
        use_container_width=True
    )

    analyze_btn = st.button(
        "Analyze Imported Data",
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
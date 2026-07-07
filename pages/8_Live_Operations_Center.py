import streamlit as st

from utils.live_data import (
    DATA_SOURCE,
    CONNECTION_STATUS,
    LAST_UPDATE
)
from utils.auth_guard import require_login


require_login()

st.title("📡 Live Operations Center")

st.success("TRUEshot Live Monitoring")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Data Source",
        DATA_SOURCE
    )

with col2:
    st.metric(
        "Connection",
        CONNECTION_STATUS
    )

with col3:
    st.metric(
        "Last Update",
        str(LAST_UPDATE)
    )

st.info(
    "Waiting for live WITS connection..."
)
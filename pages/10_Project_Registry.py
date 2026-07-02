import streamlit as st

from core.session_manager import SessionManager


st.set_page_config(
    page_title="Project Registry",
    page_icon="📁",
    layout="wide"
)

context = SessionManager.get_context()

st.title("📁 Project Registry")

st.divider()

st.subheader("Current Enterprise Context")

st.write("Project:", context.current_project)

st.write("Operator:", context.current_operator)

st.write("Rig:", context.current_rig)

st.write("Well:", context.current_well)

st.write("Run:", context.current_run)

st.write("Shift:", context.current_shift)

st.divider()

st.info(
    "No project loaded."
)

st.metric(
    "Project ID",
    context.active_project_id or "-"
)


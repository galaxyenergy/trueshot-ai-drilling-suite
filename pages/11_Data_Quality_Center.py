import streamlit as st

from core.session_manager import SessionManager
from services.import_service import ImportService

st.set_page_config(
    page_title="Data Quality Center",
    page_icon="📊",
    layout="wide"
)

context = SessionManager.get_context()

st.title("📊 Data Quality Center")

uploaded_file = st.file_uploader(
    "Select WellData Shift Export",
    type=["xlsx", "xls", "csv"]
)

if uploaded_file:

    dataset = ImportService.import_file(uploaded_file)

    st.success("Shift Export Imported")

    st.dataframe(dataset.raw_dataframe.head())
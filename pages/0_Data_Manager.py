import streamlit as st
import pandas as pd

st.title("📂 Data Manager")

uploaded_file = st.file_uploader(
    "Upload Historical Drilling CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.session_state["master_df"] = df

    st.success(f"Loaded {len(df):,} rows")

    st.dataframe(df.head())
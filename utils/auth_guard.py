import streamlit as st


def require_login():
    if not st.session_state.get("authenticated", False):
        st.warning("Please log in from the TrueShot Home page first.")
        st.stop()
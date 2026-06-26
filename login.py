import streamlit as st

def login_screen():

    st.title("🚀 Galaxy AI Drilling Intelligence Suite")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if (
            username == "admin"
            and
            password == "galaxy2026"
        ):

            st.session_state["authenticated"] = True
            st.rerun()

        else:
            st.error("Invalid username or password")
            
            
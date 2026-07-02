import streamlit as st
from .app_context import AppContext

class SessionManager:

    SESSION_KEY = "app_context"


    @staticmethod
    def initialize():

        if SessionManager.SESSION_KEY not in st.session_state:

            st.session_state[SessionManager.SESSION_KEY] = AppContext()


    @staticmethod
    def get_context():

        SessionManager.initialize()

        return st.session_state[SessionManager.SESSION_KEY]


    @staticmethod
    def save_context(context):

        st.session_state[SessionManager.SESSION_KEY] = context
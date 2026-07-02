import streamlit as st

from utils import live_data


def get_mwd_data():

    if live_data.DATA_SOURCE == "CSV":
        return st.session_state.get("mwd_df")

    return live_data.LIVE_DF


def get_survey_data():

    if live_data.DATA_SOURCE == "CSV":
        return st.session_state.get("survey_df")

    return live_data.LIVE_SURVEY_DF
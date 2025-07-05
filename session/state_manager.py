import streamlit as st
import pandas as pd

def initialize_session_state():
    if "api_data" not in st.session_state:
        st.session_state.api_data = pd.DataFrame()
    if "charts" not in st.session_state:
        st.session_state.charts = []
    if "api_fetched" not in st.session_state:
        st.session_state.api_fetched = False
    if "api_url" not in st.session_state:
        st.session_state.api_url = ""
    if "params_input" not in st.session_state:
        st.session_state.params_input = "{}"
    if "chart_configured" not in st.session_state:
        st.session_state.chart_configured = False
    if "chart_title" not in st.session_state:
        st.session_state.chart_title = ""
    if "cameras" not in st.session_state:
        st.session_state.cameras = []
    if "db_data_loaded" not in st.session_state:
        st.session_state.db_data_loaded = False
    if "chart_data" not in st.session_state:
        st.session_state.chart_data = {}
    if 'show_cameras' not in st.session_state:
        st.session_state.show_cameras = True
    if 'db_type' not in st.session_state:
        st.session_state.db_type = ""
    if 'db_data' not in st.session_state:
        st.session_state.db_data = pd.DataFrame()

import pandas as pd
import datetime
import requests
import streamlit as st

def fetch_data_from_api(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        json_data = response.json()
        data = pd.json_normalize(json_data)
        data["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return data
    except Exception as e:
        st.error(f"Błąd API: {e}")
        return pd.DataFrame()

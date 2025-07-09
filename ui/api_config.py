import streamlit as st
import uuid
import pandas as pd
import json
from fetchers.api_fetcher import fetch_data_from_api

def api_config_ui():
    st.sidebar.header("Konfiguracja API")
    with st.sidebar.expander("📘 Pomoc: Jak skonfigurować API"):
        st.markdown("""
        **Opis pól:**

        - **URL API** – Pełny adres endpointu (np. `https://example.com/api/data`)
        - **Parametry zapytania (JSON)** – Dane w formacie JSON, np.:
          ```json
          {
            "sensor_id": "abc123",
            "from": "2024-01-01",
            "to": "2024-01-07"
          }
          ```

        **Wskazówki:**

        - Sprawdź dokumentację API, jeśli nie znasz struktury zapytania i odpowiedzi.
        """)

    api_url = st.sidebar.text_input(
        "URL API",
        value=st.session_state.api_url,
        help="Adres końcowego punktu API (np. https://example.com/api/data)"
    )

    params_input = st.sidebar.text_area(
        "Parametry zapytania (JSON)",
        value=st.session_state.params_input,
        help='Wprowadź parametry w formacie JSON, np.: {"sensor_id": "abc123"}'
    )

    try:
        params = json.loads(params_input)
    except json.JSONDecodeError:
        st.error("Nieprawidłowy format JSON")
        params = {}

    if st.sidebar.button("Pobierz dane z API"):
        new_data = fetch_data_from_api(api_url, params)
        if not new_data.empty:
            st.session_state.api_data = new_data
            st.session_state.api_fetched = True
            st.session_state.api_url = api_url
            st.session_state.params_input = params_input
            st.sidebar.success("Dane pobrane!")

    if st.session_state.api_fetched:
        st.sidebar.header("Konfiguracja wykresu")
        chart_title = st.sidebar.text_input("Nazwa wykresu", value=st.session_state.chart_title)
        chart_type = st.sidebar.selectbox("Typ wykresu", ["Liniowy", "Słupkowy", "Punktowy"])
        x_column = st.sidebar.selectbox("Kolumna X", ["timestamp"] + list(st.session_state.api_data.columns))
        y_column = st.sidebar.selectbox("Kolumna Y", st.session_state.api_data.columns)
        max_points = st.sidebar.number_input("Maksymalna liczba punktów", min_value=1,value=10,max_value=100)

        if st.sidebar.button("Dodaj wykres"):
            chart_id = str(uuid.uuid4())
            st.session_state.charts.append({
                "id": chart_id,
                "title": chart_title,
                "source": "API",
                "type": chart_type,
                "x_column": x_column,
                "y_column": y_column,
                "api_url": api_url,
                "params": params,
                "max_points": max_points
            })
            st.session_state.chart_data[chart_id] = pd.DataFrame()
            st.session_state.api_fetched = False
            st.session_state.chart_title = ""
            st.session_state.api_url = ""
            st.session_state.params_input = "{}"
            st.rerun()

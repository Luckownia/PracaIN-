import streamlit as st
import uuid
import pandas as pd
from urllib.parse import quote_plus
from fetchers.database_fetcher import fetch_data_from_db

def db_config_ui():
    st.sidebar.header("Konfiguracja Bazy Danych")

    with st.sidebar.expander("📘 Pomoc: Jak skonfigurować połączenie z bazą danych"):
        st.markdown("""
        **Opis pól:**

        - **Typ bazy danych** – Wybierz typ bazy danych, np. `PostgreSQL`, `MySQL`, `MongoDB`
        - **Host** – Adres serwera bazy danych (np. `localhost`, `db.myhost.com`)
        - **Port** – Standardowe porty:
            - PostgreSQL: `5432`
            - MySQL: `3306`
            - MongoDB: `27017`
        - **Użytkownik / Hasło** – Dane logowania do bazy
        - **Nazwa bazy** – Nazwa konkretnej bazy, np. `sensors`
        """)


    db_type = st.sidebar.selectbox("Typ bazy danych", ["PostgreSQL", "MySQL", "MongoDB"],help="Wybierz typ bazy danych, z której korzystasz")
    st.session_state.db_type = db_type

    if db_type == "PostgreSQL":
        default_port = "5432"
    elif db_type == "MySQL":
        default_port = "3306"
    elif db_type == "MongoDB":
        default_port = "27017"
    else:
        default_port = ""

    host = st.sidebar.text_input("Host bazy danych",help="Adres serwera")
    port = st.sidebar.text_input("Port", default_port, help="Np. 5432 (PostgreSQL), 3306 (MySQL), 27017 (MongoDB)")
    user = st.sidebar.text_input("Użytkownik",help="Nazwa użytkownika bazy danych")
    password = st.sidebar.text_input("Hasło", type="password",help="Hasło użytkownika")
    database = st.sidebar.text_input("Nazwa bazy danych",help="Nazwa konkretnej bazy danych")

    if db_type == "MongoDB":
        collection_name = st.sidebar.text_input("Kolekcja (MongoDB)", "")
    else:
        collection_name = ""

    query = st.sidebar.text_area(
        "Zapytanie SQL",
        help="Wprowadź pełne zapytanie SELECT, np.: SELECT * FROM sensors WHERE timestamp > NOW() - INTERVAL '1 day'.\nPamiętaj: tylko zapytania odczytujące dane są dozwolone."
    )

    if db_type == "PostgreSQL":
        connection_string = f"postgresql://{user}:{quote_plus(password)}@{host}:{port}/{database}"
    elif db_type == "MySQL":
        connection_string = f"mysql://{user}:{quote_plus(password)}@{host}:{port}/{database}"
    elif db_type == "MongoDB":
        if user and password:
            connection_string = f"mongodb://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{database}"
        else:
            connection_string = f"mongodb://{host}:{port}/{database}"
    else:
        connection_string = ""

    if st.sidebar.button("Pobierz dane z bazy"):
        db_data = fetch_data_from_db(connection_string, query, db_type, collection_name)
        if not db_data.empty:
            st.session_state.db_data = db_data
            st.session_state.db_data_loaded = True
            st.sidebar.success("Dane zostały pobrane!")

    if st.session_state.db_data_loaded:
        st.sidebar.header("Konfiguracja wykresu")
        chart_title = st.sidebar.text_input("Nazwa wykresu", value=st.session_state.chart_title)
        chart_type = st.sidebar.selectbox("Typ wykresu", ["Liniowy", "Słupkowy", "Punktowy"])
        x_column = st.sidebar.selectbox("Kolumna X", ["timestamp"] + list(st.session_state.db_data.columns))
        y_column = st.sidebar.selectbox("Kolumna Y", st.session_state.db_data.columns)
        max_points = st.sidebar.number_input("Maksymalna liczba punktów", min_value=1, value=10, max_value=100)

        if st.sidebar.button("Dodaj wykres"):
            if chart_title:
                chart_id = str(uuid.uuid4())
                st.session_state.charts.append({
                    "id": chart_id,
                    "title": chart_title,
                    "source": "Baza danych",
                    "type": chart_type,
                    "x_column": x_column,
                    "y_column": y_column,
                    "db_connection": connection_string,
                    "query": query,
                    "collection_name": collection_name,
                    "max_points": max_points
                })
                st.session_state.chart_data[chart_id] = pd.DataFrame()
                st.sidebar.success(f"Wykres '{chart_title}' dodany!")
                st.session_state.db_data_loaded = False
                st.session_state.chart_title = ""
                st.rerun()

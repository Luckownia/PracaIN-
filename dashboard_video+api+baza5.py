import streamlit as st
import time
import datetime
import pandas as pd
import requests
import plotly.graph_objs as go
import uuid
from sqlalchemy import create_engine
from pymongo import MongoClient
from urllib.parse import quote_plus

# Inicjalizacja sesji
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


st.title("📊 Dashboard - Wiele Źródeł Danych")

# Funkcja pobierania danych z API
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

# Funkcja pobierania danych z bazy
def fetch_data_from_db(connection_string, query, db_type, collection_name=None):
    try:
        if db_type == "MongoDB":
            client = MongoClient(connection_string)
            db = client.get_database()
            collection = db[collection_name]
            data = pd.DataFrame(list(collection.find()))
            if "_id" in data.columns:
                data.drop("_id", axis=1, inplace=True)
        else:
            engine = create_engine(connection_string)
            data = pd.read_sql(query, engine)
        data["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return data
    except Exception as e:
        st.error(f"Błąd bazy danych: {e}")
        return pd.DataFrame()

# **WYBÓR KONFIGURACJI**
config_choice = st.sidebar.radio("Wybierz konfigurację", ["API", "Baza danych", "Kamery"])

# **API**
if config_choice == "API":
    st.sidebar.header("Konfiguracja API")
    api_url = st.sidebar.text_input("URL API", value=st.session_state.api_url)
    params_input = st.sidebar.text_area("Parametry zapytania (JSON)", value=st.session_state.params_input)
    params = eval(params_input)

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
        max_points = st.sidebar.number_input("Maksymalna liczba punktów", min_value=1, value=100, step=1)

        if st.sidebar.button("Dodaj wykres"):
            chart_id = str(uuid.uuid4())  # Unikalny identyfikator wykresu
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
            st.session_state.chart_title = ""
            st.session_state.api_url = ""
            st.session_state.params_input = "{}"
            st.session_state.api_fetched = False
            st.rerun()  # Odświeżenie interfejsu

        # **Baza danych**
elif config_choice == "Baza danych":
    st.sidebar.header("Konfiguracja Bazy Danych")

    db_type = st.sidebar.selectbox("Typ bazy danych", ["PostgreSQL", "MySQL", "MongoDB"])
    st.session_state.db_type = db_type  # Zapisanie typu bazy danych w sesji

    # Parametry połączenia
    host = st.sidebar.text_input("Host bazy danych")
    port = st.sidebar.text_input("Port bazy danych",
                                 "5432" if db_type == "PostgreSQL" else "3306")  # Domyślny port zależny od bazy
    user = st.sidebar.text_input("Użytkownik")
    password = st.sidebar.text_input("Hasło", type="password")
    database = st.sidebar.text_input("Nazwa bazy danych")

    # Dodatkowe ustawienia dla MongoDB
    if db_type == "MongoDB":
        collection_name = st.sidebar.text_input("Kolekcja (MongoDB)", "")
    else:
        collection_name = ""

    query = st.sidebar.text_area("Zapytanie SQL")

    # Generowanie connection string
    if db_type == "PostgreSQL":
        connection_string = f"postgresql://{user}:{quote_plus(password)}@{host}:{port}/{database}"
    elif db_type == "MySQL":
        connection_string = f"mysql://{user}:{quote_plus(password)}@{host}:{port}/{database}"
    elif db_type == "MongoDB":
        connection_string = f"mongodb://{user}:{quote_plus(password)}@{host}:{port}/{database}"
    else:
        connection_string = ""

    # **Przycisk Pobierz dane**
    if st.sidebar.button("Pobierz dane z bazy"):
        db_data = fetch_data_from_db(connection_string, query, db_type, collection_name)
        if not db_data.empty:
            st.session_state.db_data = db_data
            st.session_state.db_data_loaded = True  # Flaga, która mówi, że dane zostały pobrane
            st.sidebar.success("Dane zostały pomyślnie pobrane z bazy danych!")

    # Konfiguracja wykresu (po pobraniu danych z bazy)
    if st.session_state.db_data_loaded and not st.session_state.chart_configured:
        st.sidebar.header("Krok 2: Konfiguracja wykresu")
        chart_title = st.sidebar.text_input("Nazwa wykresu", value=st.session_state.chart_title)  # Nazwa wykresu
        chart_type = st.sidebar.selectbox("Typ wykresu", ["Liniowy", "Słupkowy", "Punktowy"])
        x_column = st.sidebar.selectbox("Kolumna X", ["timestamp"] + list(st.session_state.db_data.columns))
        y_column = st.sidebar.selectbox("Kolumna Y", st.session_state.db_data.columns)
        max_points = st.sidebar.number_input("Maksymalna liczba punktów", min_value=1, value=10,max_value=100, step=1)


        if st.sidebar.button("Dodaj wykres"):
            if chart_title:  # Jeśli użytkownik podał nazwę wykresu
                chart_id = str(uuid.uuid4())  # Unikalny identyfikator wykresu

                st.session_state.charts.append({
                    "id": chart_id,
                    "title": chart_title,
                    "source": "Baza danych",
                    "type": chart_type,
                    "x_column": x_column,
                    "y_column": y_column,
                    "db_connection": connection_string,
                    "query": query,
                    "max_points": max_points
                })

                st.session_state.chart_data[chart_id] = pd.DataFrame()
                st.sidebar.success(f"Wykres '{chart_title}' został dodany!")  # Komunikat o dodaniu wykresu
                st.session_state.db_data_loaded = False  # Resetowanie danych po dodaniu wykresu
                st.session_state.chart_configured = False  # Resetowanie formularza, aby można było dodać nowy wykres

                st.session_state.chart_title = ""
                st.session_state.db_data_loaded = False
                st.session_state.chart_configured = False
                st.session_state.db_data = pd.DataFrame()
                st.rerun()  # Odświeżenie interfejsu

# **Kamery**
elif config_choice == "Kamery":
    st.sidebar.header("Dodaj Kamery")
    camera_url = st.sidebar.text_input("Dodaj kamerę URL")
    if st.sidebar.button("Dodaj kamerę") and camera_url:
        st.session_state.cameras.append(camera_url)
        st.sidebar.success(f"Kamera {camera_url} dodana!")

# **UKŁAD DASHBOARDU**
placeholder = st.empty()

while True:
    with placeholder.container():
        st.subheader("📊 Wykresy")
        if st.session_state.charts:
            for idx, chart in enumerate(st.session_state.charts):
                chart_id = chart["id"]  # Pobieramy ID wykresu
                st.write(f"### Wykres {idx + 1} - {chart['title']} - Źródło: {chart['source']}")

                # **Pobieranie danych dla API**
                if chart["source"] == "API":
                    new_data = fetch_data_from_api(chart["api_url"], chart["params"])  # Pobierz nowe dane
                    if not new_data.empty:
                        st.session_state.chart_data[chart_id] = pd.concat(
                            [st.session_state.chart_data[chart_id], new_data], ignore_index=True
                        )

                    data = st.session_state.chart_data[chart_id]  # Pobranie danych dla tego wykresu

                # **Pobieranie danych dla Bazy Danych**
                elif chart["source"] == "Baza danych":
                    if st.session_state.db_type == "MongoDB":
                        new_data = fetch_data_from_db(chart["db_connection"], chart["query"], st.session_state.db_type, chart.get("collection_name", ""))
                    else:
                        new_data = fetch_data_from_db(chart["db_connection"], chart["query"], st.session_state.db_type)

                    if not new_data.empty:
                        st.session_state.chart_data[chart_id] = pd.concat(
                            [st.session_state.chart_data[chart_id], new_data], ignore_index=True
                        )

                    data = st.session_state.chart_data[chart_id]  # Pobranie danych dla tego wykresu

                # **Ograniczenie liczby punktów**
                if "max_points" in chart and len(data) > chart["max_points"]:
                    data = data.tail(chart["max_points"])

                # **Tworzenie wykresu**
                fig = go.Figure()
                if chart["type"] == "Liniowy":
                    fig.add_trace(go.Scatter(x=data[chart["x_column"]], y=data[chart["y_column"]], mode="lines+markers"))
                elif chart["type"] == "Słupkowy":
                    fig.add_trace(go.Bar(x=data[chart["x_column"]], y=data[chart["y_column"]]))
                elif chart["type"] == "Punktowy":
                    fig.add_trace(go.Scatter(x=data[chart["x_column"]], y=data[chart["y_column"]], mode="markers"))

                st.plotly_chart(fig, use_container_width=True, key=str(uuid.uuid4()))



        # **PODGLĄD KAMER**
        st.subheader("📹 Podgląd kamer")
        camera_container = st.empty()
        with camera_container.container():
            for camera in st.session_state.cameras:
                st.image(f"{camera}?nocache={datetime.datetime.now().timestamp()}", use_container_width=True)

    time.sleep(1)  # Odświeżanie co sekundę


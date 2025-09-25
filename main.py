import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from fetchers.camera_fetcher import release_all_cameras
from session.state_manager import initialize_session_state
from fetchers.api_fetcher import fetch_data_from_api
from fetchers.database_fetcher import fetch_data_from_db
from fetchers.camera_fetcher import get_camera_frame
from charts.plotter import render_chart
import pymysql
pymysql.install_as_MySQLdb()

# Ustawienia strony
st.set_page_config(layout="wide")

# Inicjalizacja sesji
initialize_session_state()

st.title("📊 Twój Dashboard")

# Odświeżanie aplikacji
st_autorefresh(interval=5000, limit=None, key="data_refresh")

config_choice = st.sidebar.radio("Wybierz konfigurację", ["API", "Baza danych", "Kamery"])

# --- Obsługa API ---
if config_choice == "API":
    from ui.api_config import api_config_ui
    api_config_ui()

# --- Obsługa Bazy Danych ---
elif config_choice == "Baza danych":
    from ui.db_config import db_config_ui
    db_config_ui()

# --- Obsługa Kamer ---
elif config_choice == "Kamery":
    from ui.camera_config import camera_config_ui
    camera_config_ui()

st.subheader("📈 Dashboard")

# Wszystko w jednej liście
items = st.session_state.dashboard_items
num_cols = 3

for i in range(0, len(items), num_cols):
    cols = st.columns(num_cols)
    for j, item in enumerate(items[i:i + num_cols]):
        idx = i + j  # globalny indeks w dashboard_items
        with cols[j]:
            # --- Wykres ---
            if item["kind"] == "chart":
                chart = item["data"]
                chart_id = chart["id"]

                # Pobieranie nowych danych
                if chart["source"] == "API":
                    new_data = fetch_data_from_api(chart["api_url"], chart["params"])
                else:
                    new_data = fetch_data_from_db(
                        chart["db_connection"], chart["query"],
                        st.session_state.db_type, chart.get("collection_name", "")
                    )

                if not new_data.empty:
                    st.session_state.chart_data[chart_id] = pd.concat(
                        [st.session_state.chart_data[chart_id], new_data], ignore_index=True
                    )

                data = st.session_state.chart_data[chart_id]
                if "max_points" in chart and len(data) > chart["max_points"]:
                    data = data.tail(chart["max_points"])

                fig = render_chart(chart, data)
                st.plotly_chart(fig, use_container_width=True)

                # Przyciski sterujące
                col_btns = st.columns([1, 1, 2])
                with col_btns[0]:
                    if st.button("⬅️", key=f"left_{idx}") and idx > 0:
                        items[idx-1], items[idx] = items[idx], items[idx-1]
                        st.session_state.dashboard_items = items
                        st.rerun()
                with col_btns[1]:
                    if st.button("➡️", key=f"right_{idx}") and idx < len(items) - 1:
                        items[idx+1], items[idx] = items[idx], items[idx+1]
                        st.session_state.dashboard_items = items
                        st.rerun()
                with col_btns[2]:
                    if st.button(f"🗑️ Usuń {chart['title']}", key=f"delete_chart_{chart_id}"):
                        del st.session_state.chart_data[chart_id]
                        del st.session_state.dashboard_items[idx]
                        st.rerun()

            # --- Kamera ---
            elif item["kind"] == "camera":
                camera = item["data"]
                st.markdown(f"**Kamera:** `{camera}`")

                # Podgląd kamery
                if any(ext in camera.lower() for ext in [".jpg", ".jpeg", ".mjpg", "snapshot", "faststream"]):
                    st.image(camera, use_container_width=True)
                else:
                    frame = get_camera_frame(camera)
                    if frame is not None:
                        st.image(frame, channels="RGB", use_container_width=True)
                    else:
                        st.error(f"❌ Nie udało się pobrać obrazu z kamery: {camera}")

                # Przyciski sterujące
                col_btns = st.columns([1, 1, 2])
                with col_btns[0]:
                    if st.button("⬅️", key=f"left_{idx}") and idx > 0:
                        items[idx-1], items[idx] = items[idx], items[idx-1]
                        st.session_state.dashboard_items = items
                        st.rerun()
                with col_btns[1]:
                    if st.button("➡️", key=f"right_{idx}") and idx < len(items) - 1:
                        items[idx+1], items[idx] = items[idx], items[idx+1]
                        st.session_state.dashboard_items = items
                        st.rerun()
                with col_btns[2]:
                    if st.button("🗑️ Usuń kamerę", key=f"delete_camera_{idx}"):
                        del st.session_state.dashboard_items[idx]
                        st.rerun()

# Zwolnienie zasobów gdy brak kamer w dashboardzie
if not any(item["kind"] == "camera" for item in st.session_state.dashboard_items):
    release_all_cameras()

